package cug.paleogpt.demo.util;

import cug.paleogpt.demo.common.Constants;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;
import redis.clients.jedis.JedisPoolConfig;

public class JedisUtil {
    private static JedisPool jedisPool;

    static {
        // 创建 JedisPool 配置
        JedisPoolConfig poolConfig = new JedisPoolConfig();
        poolConfig.setMaxTotal(128);  // 最大连接数
        poolConfig.setMaxIdle(128);   // 最大空闲连接数
        poolConfig.setMinIdle(16);    // 最小空闲连接数
        poolConfig.setMaxWaitMillis(200);   //最大等待时间
        poolConfig.setTestOnBorrow(true); // 连接池获取连接时是否进行校验

        // 创建 JedisPool
        jedisPool = new JedisPool(poolConfig, Constants.REDIS_IP,Constants.REDIS_PORT);
    }

    public static void set(String key, String value){
        Jedis jedis = jedisPool.getResource();
        jedis.set(key, value);
    }

    public static String get(String key){
        Jedis jedis = jedisPool.getResource();
        return jedis.get(key);
    }
}
