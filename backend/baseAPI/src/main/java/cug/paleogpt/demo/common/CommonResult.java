package cug.paleogpt.demo.common;

import lombok.AllArgsConstructor;
import lombok.Data;
import org.springframework.http.HttpStatus;

import java.util.HashMap;

/**
 * 通用返回结果
 *
 * @author xw
 */
@Data
@AllArgsConstructor
public class CommonResult {
    private Integer status;
    private String message;
    private HashMap<String, Object> data;

    public static CommonResult success() {
        return new CommonResult(200, "success", null);
    }

    public static CommonResult success(String message) {
        return new CommonResult(200, message, null);
    }

    public static CommonResult success(HashMap<String, Object> data) {
        return new CommonResult(200, "success", data);
    }

    public static CommonResult success(String message, HashMap<String, Object> data) {
        return new CommonResult(200, message, data);
    }

    public static CommonResult error() {
        return new CommonResult(500, HttpStatus.INTERNAL_SERVER_ERROR.getReasonPhrase(), null);
    }

    public static CommonResult error(String message) {
        return new CommonResult(500, message, null);
    }
}
