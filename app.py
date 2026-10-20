<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Geometry Dash Mini</title>
<style>
*{box-sizing:border-box}
body{margin:0;background:#090d24;color:white;text-align:center;font-family:Arial}
h1{color:#00ffff;text-shadow:0 0 15px cyan}
canvas{width:96%;max-width:900px;border:3px solid cyan;border-radius:8px}
button{padding:12px 24px;margin:8px;background:#00ffff;border:0;border-radius:8px;font-weight:bold;font-size:17px}
p{color:#d5eaff}
</style>
</head>
<body>
<h1>GEOMETRY DASH</h1>
<p>SPACE / ↑ / chạm màn hình để nhảy</p>
<canvas id="game" width="900" height="400"></canvas>
<br><button onclick="start()">START / RESTART</button>
<p id="score">Điểm: 0</p>
<script>
const c=document.getElementById("game"),ctx=c.getContext("2d");
const ground=330;
let p,obs,score,speed,alive,started,last=0,timer=0;
let audio;
function beep(f=500){
 try{
  audio ||= new (window.AudioContext||window.webkitAudioContext)();
  if(audio.state==="suspended")audio.resume();
  let o=audio.createOscillator(),g=audio.createGain();
  o.frequency.value=f;g.gain.value=.05;
  o.connect(g);g.connect(audio.destination);o.start();
  g.gain.exponentialRampToValueAtTime(.001,audio.currentTime+.12);
  o.stop(audio.currentTime+.12);
 }catch(e){}
}
function start(){
 p={x:100,y:295,s:35,vy:0,rot:0,grounded:true};
 obs=[];score=0;speed=6;alive=true;started=true;
 timer=50;last=0;
 requestAnimationFrame(loop);
}
function jump(){
 if(!started){start();return}
 if(alive&&p.grounded){
  p.vy=-12.5;p.grounded=false;beep();
 }
}
addEventListener("keydown",e=>{
 if(["Space","ArrowUp","KeyW"].includes(e.code)){
  e.preventDefault();
  if(!e.repeat)jump();
 }
 if(e.code==="Enter"&&!alive)start();
});
c.addEventListener("pointerdown",e=>{e.preventDefault();jump()});
function update(dt){
 if(!alive)return;
 let d=dt/16.667;
 p.vy+=.65*d;p.y+=p.vy*d;
 if(p.y+p.s>=ground){
  p.y=ground-p.s;p.vy=0;p.grounded=true;
  p.rot=Math.round(p.rot/(Math.PI/2))*(Math.PI/2);
 }else{p.grounded=false;p.rot+=.09*d}
 timer-=d;
 if(timer<=0){
  obs.push({x:920,w:32,h:35+Math.random()*15});
  timer=65+Math.random()*35;
 }
 for(let o of obs){
  o.x-=speed*d;
  if(p.x+29>o.x+5&&p.x+6<o.x+o.w-5&&
     p.y+p.s-5>ground-o.h){
   alive=false;beep(100);
  }
 }
 obs=obs.filter(o=>o.x+o.w>0);
 score+=d;speed=Math.min(10,6+score/500);
 document.getElementById("score").textContent="Điểm: "+Math.floor(score);
}
function draw(){
 ctx.clearRect(0,0,900,400);
 ctx.fillStyle="#10152f";ctx.fillRect(0,0,900,400);
 ctx.strokeStyle="#26345b";
 for(let x=0;x<900;x+=40){
  ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,ground);ctx.stroke();
 }
 for(let y=10;y<ground;y+=40){
  ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(900,y);ctx.stroke();
 }
 ctx.fillStyle="#193d55";ctx.fillRect(0,ground,900,70);
 ctx.fillStyle="#00ffff";ctx.fillRect(0,ground,900,3);
 for(let o of obs){
  ctx.fillStyle="#ff3864";ctx.shadowColor="#ff1744";ctx.shadowBlur=12;
  ctx.beginPath();ctx.moveTo(o.x,ground);
  ctx.lineTo(o.x+o.w/2,ground-o.h);
  ctx.lineTo(o.x+o.w,ground);ctx.closePath();ctx.fill();
 }
 ctx.shadowBlur=0;
 ctx.save();
 ctx.translate(p.x+p.s/2,p.y+p.s/2);
 ctx.rotate(p.rot);
 ctx.fillStyle="#00ff9d";ctx.shadowColor="#00ff9d";ctx.shadowBlur=15;
 ctx.fillRect(-p.s/2,-p.s/2,p.s,p.s);
 ctx.shadowBlur=0;
 ctx.fillStyle="#10152f";
 ctx.fillRect(-9,-7,5,7);ctx.fillRect(4,-7,5,7);
 ctx.restore();
 if(!alive){
  ctx.fillStyle="rgba(0,0,0,.7)";ctx.fillRect(0,0,900,400);
  ctx.textAlign="center";
  ctx.fillStyle="#ff3864";ctx.font="bold 48px Arial";
  ctx.fillText("GAME OVER",450,180);
  ctx.fillStyle="white";ctx.font="22px Arial";
  ctx.fillText("Điểm: "+Math.floor(score),450,220);
  ctx.fillText("Nhấn START để chơi lại",450,260);
 }
}
function loop(now){
 if(!started)return;
 let dt=last?Math.min(now-last,40):16.667;
 last=now;update(dt);draw();
 if(alive)requestAnimationFrame(loop);
}
start();
</script>
</body>
</html>
