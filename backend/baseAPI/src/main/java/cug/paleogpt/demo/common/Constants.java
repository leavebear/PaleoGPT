package cug.paleogpt.demo.common;

/**
 * 常量
 *
 * @author xw
 */
public class Constants {
    /**
     * redis键值对过期时间（秒）
     */
    public static final Integer REDIS_TIMEOUT = 60 * 60 * 7;

    /**
     * redis服务IP
     */
    public static final String REDIS_IP = "localhost";

    /**
     * redis服务端口
     */
    //
    public static final Integer REDIS_PORT = 6379;

    /**
     * minio服务URL
     */
    public static final String MINIO_URL = "http://localhost:9000";

}
