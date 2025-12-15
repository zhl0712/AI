const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;

app.use(bodyParser.json());

// 生成随机键值对的函数（值为数字）
function generateRandomData(count = 5) {
    const data = {};
    const possibleKeys = ['id', 'name', 'value', 'score', 'status', 'color', 'size', 'price', 'quantity', 'active'];
    
    for (let i = 0; i < count; i++) {
        const randomKey = possibleKeys[Math.floor(Math.random() * possibleKeys.length)];
        data[randomKey] = Math.floor(Math.random() * 1000); // 生成0-999的随机整数
    }
    return data;
}

app.get('/api', (req, res) => {
    res.json({
        status: 'success',
        message: 'GET请求已处理',
        randomData: generateRandomData(),
        timestamp: new Date().toISOString()
    });
});

app.post('/api', (req, res) => {
    res.json({
        status: 'success',
        message: 'POST请求已处理', 
        randomData: generateRandomData(),
        timestamp: new Date().toISOString()
    });
});

app.listen(port, '0.0.0.0', () => {
    console.log(`服务器运行在 http://localhost:${port}`);
    console.log(`外部访问地址: http://${getPublicIp()}:${port}`);
});

// 获取公网IP的函数（简化版）
function getPublicIp() {
    try {
        // 注意：这个方法需要服务器能访问外网
        return require('child_process').execSync('curl ifconfig.me').toString().trim();
    } catch (e) {
        return '自动获取失败，请手动设置';
    }
}

// 添加基本的安全中间件
const helmet = require('helmet');
app.use(helmet());

// 添加CORS支持（如需跨域访问）
const cors = require('cors');
// 更新CORS配置
app.use(cors({
    origin: true, // 动态根据请求来源设置
    methods: ['GET', 'POST', 'OPTIONS', 'PUT', 'DELETE'],
    allowedHeaders: ['Content-Type', 'Authorization'],
    maxAge: 86400, // 预检请求缓存时间
    preflightContinue: false
}));

// 更新CORS配置为更严格的设置
app.use(cors({
    origin: function(origin, callback) {
        // 允许所有来源或特定来源
        const allowedOrigins = ['http://example.com', 'http://localhost:*'];
        if (!origin || allowedOrigins.some(o => origin.match(new RegExp(o.replace('*', '.*'))))) {
            callback(null, true);
        } else {
            callback(new Error('Not allowed by CORS'));
        }
    },
    methods: ['GET', 'POST', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization'],
    exposedHeaders: ['Content-Length', 'X-Request-Id'],
    credentials: false,
    maxAge: 86400
}));

// 确保OPTIONS处理在所有路由之前
app.options('*', cors());

// 添加OPTIONS方法处理
app.options('/api', (req, res) => {
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    res.status(204).end();
});