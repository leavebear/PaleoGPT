import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RequestCallback;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.Map;
import java.util.concurrent.CompletableFuture;

@RestController
public class ChatController {

    private final RestTemplate restTemplate = new RestTemplate();

    @GetMapping("/api/QAsystemStream")
    public SseEmitter streamChat(@RequestParam String message) {
        SseEmitter emitter = new SseEmitter(60_000L); // 设置 60 秒超时
        String apiUrl = "http://192.168.148.10:8000/v1/chat/completions";

        CompletableFuture.runAsync(() -> {
            try {
                // 构建请求头
                HttpHeaders headers = new HttpHeaders();
                headers.setContentType(MediaType.APPLICATION_JSON);

                // 构建请求体
                Map<String, Object> requestData = Map.of(
                        "model", "qwq-32B",
                        "messages", new Object[]{
                                Map.of("role", "user", "content", message)
                        },
                        "stream", true
                );

                HttpEntity<Map<String, Object>> requestEntity = new HttpEntity<>(requestData, headers);

                // 发起流式请求
                RequestCallback requestCallback = restTemplate.httpEntityCallback(requestEntity, String.class);
                restTemplate.execute(apiUrl, HttpMethod.POST, requestCallback, clientHttpResponse -> {
                    try (BufferedReader reader = new BufferedReader(new InputStreamReader(clientHttpResponse.getBody()))) {
                        String line;
                        while ((line = reader.readLine()) != null) {
                            if (!line.trim().isEmpty()) {
                                emitter.send(SseEmitter.event().data(line));
                            }
                        }
                        emitter.complete();
                    } catch (Exception e) {
                        emitter.completeWithError(e);
                    }
                    return null;
                });

            } catch (Exception e) {
                emitter.completeWithError(e);
            }
        });

        return emitter;
    }
}
