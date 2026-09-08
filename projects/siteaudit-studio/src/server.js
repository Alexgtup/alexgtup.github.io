import path from 'node:path';
import { fileURLToPath } from 'node:url';
import express from 'express';
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';
import { auditSite } from './audit.js';

const __filename=fileURLToPath(import.meta.url); const __dirname=path.dirname(__filename); const publicDir=path.resolve(__dirname,'../public'); const port=Number(process.env.PORT||3000);
const app=express(); app.set('trust proxy',1); app.disable('x-powered-by');
app.use(helmet({contentSecurityPolicy:{directives:{defaultSrc:["'self'"],scriptSrc:["'self'"],styleSrc:["'self'"],imgSrc:["'self'",'data:'],connectSrc:["'self'"],objectSrc:["'none'"],baseUri:["'self'"],frameAncestors:["'none'"]}},crossOriginEmbedderPolicy:false}));
app.use(express.json({limit:'16kb'}));
const auditLimiter=rateLimit({windowMs:10*60*1000,limit:12,standardHeaders:'draft-7',legacyHeaders:false,message:{error:'Слишком много аудитов. Попробуйте позже.'}});
app.get('/api/health',(_req,res)=>res.json({ok:true,service:'siteaudit-studio',version:1}));
app.post('/api/audit',auditLimiter,async(req,res)=>{const url=typeof req.body?.url==='string'?req.body.url.trim():''; if(!url){res.status(400).json({error:'Передайте URL сайта'});return;} const started=Date.now(); try{const report=await auditSite(url);res.json({...report,serverDurationMs:Date.now()-started});}catch(error){const message=error instanceof Error?error.message:'Не удалось выполнить аудит'; const isClientError=/URL|HTTP|HTTPS|локаль|приват|служеб|DNS|HTML|таймаут|лимит/i.test(message);res.status(isClientError?400:502).json({error:message});}});
app.use(express.static(publicDir,{extensions:['html'],maxAge:process.env.NODE_ENV==='production'?'1h':0,setHeaders(res,filePath){if(filePath.endsWith('.html'))res.setHeader('Cache-Control','no-cache');}}));
app.get('*',(_req,res)=>res.sendFile(path.join(publicDir,'index.html')));
app.listen(port,'0.0.0.0',()=>console.log(`SiteAudit Studio listening on 0.0.0.0:${port}`));
