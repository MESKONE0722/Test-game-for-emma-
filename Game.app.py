# streamlit_app.py
import streamlit as st

st.set_page_config(page_title="Snow-Tropical Game", layout="wide")

# Hide Streamlit UI elements for full-screen game
st.markdown("""
<style>
    iframe { border: none; width: 100%; height: 100vh; }
    .css-1d391kg { padding: 0; }
</style>
""", unsafe_allow_html=True)

# HTML + Phaser game embedded in an iframe
game_html = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Snow‑Tropical Platformer</title>
<script src="https://cdn.jsdelivr.net/npm/phaser@3/dist/phaser.min.js"></script>
<style>body,html{margin:0;padding:0;} .button{position:absolute;bottom:20px;width:60px;height:60px;opacity:0.5;background:#555;border-radius:30px;text-align:center;line-height:60px;font-size:24px;color:#fff;user-select:none;} #left{left:20px;} #right{left:100px;} #jump{right:20px;bottom:100px;} #game-container{touch-action:none;width:100%;height:100vh;}</style>
</head><body><div id="game-container"></div><div id="left" class="button">◀</div><div id="right" class="button">▶</div><div id="jump" class="button">⭑</div>
<script>
const config = {
  type: Phaser.AUTO, parent: 'game-container', width: window.innerWidth, height: window.innerHeight,
  physics: { default: 'arcade', arcade: { gravity: { y:600 }, debug:false } },
  scene: { preload,create,update }
};
let player, platforms, score=0, scoreText, moveLeft=false, moveRight=false, doJump=false;
let game = new Phaser.Game(config);

function preload() {
  this.load.image('sky', 'https://i.imgur.com/3e5ELTf.png');
  this.load.image('platform', 'https://i.imgur.com/R3wY1ag.png');
  this.load.image('vine', 'https://i.imgur.com/ZWjvWsN.png');
  this.load.image('coconut', 'https://i.imgur.com/6WvsrdB.png');
  this.load.spritesheet('player','https://i.imgur.com/TkWfA3r.png',{frameWidth:32,frameHeight:48});
}

function create() {
  this.add.image(config.width/2,config.height/2,'sky').setScale(2);
  platforms = this.physics.add.staticGroup();
  for(let i=0;i<8;i++){
    let x=i*200, y=config.height-Phaser.Math.Between(100,200),
        key = Phaser.Math.Between(0,10)>7 ? 'vine':'platform';
    platforms.create(x,y,key);
  }
  player=this.physics.add.sprite(100,config.height-300,'player').setBounce(0.2).setCollideWorldBounds(true);
  this.anims.create({key:'left',frames:this.anims.generateFrameNumbers('player',{start:0,end:3}),frameRate:10,repeat:-1});
  this.anims.create({key:'turn',frames:[{key:'player',frame:4}],frameRate:20});
  this.anims.create({key:'right',frames:this.anims.generateFrameNumbers('player',{start:5,end:8}),frameRate:10,repeat:-1});
  this.physics.add.collider(player,platforms);
  this.coconuts=this.physics.add.group();
  platforms.children.iterate(p=>{
    this.coconuts.create(p.x+Phaser.Math.Between(-50,50),p.y-30,'coconut').body.allowGravity=false;
  });
  this.physics.add.overlap(player,this.coconuts,collect,null,this);
  scoreText=this.add.text(16,16,'Score: 0',{fontSize:'24px',fill:'#000'});
  document.getElementById('left').onpointerdown=()=>moveLeft=true;
  document.getElementById('left').onpointerup=()=>moveLeft=false;
  document.getElementById('right').onpointerdown=()=>moveRight=true;
  document.getElementById('right').onpointerup=()=>moveRight=false;
  document.getElementById('jump').onpointerdown=()=>doJump=true;
  document.getElementById('jump').onpointerup=()=>doJump=false;
}

function update() {
  if(platforms.getChildren().length<10){
    let last=platforms.getChildren().slice(-1)[0];
    let x=last.x+Phaser.Math.Between(150,250),
        y=Phaser.Math.Between(config.height-300,config.height-100),
        key=Phaser.Math.Between(0,10)>7?'vine':'platform';
    platforms.create(x,y,key);
    this.coconuts.create(x+Phaser.Math.Between(-50,50),y-30,'coconut').body.allowGravity=false;
  }
  const speed=200;
  if(moveLeft){ player.setVelocityX(-speed); player.anims.play('left', true); }
  else if(moveRight){ player.setVelocityX(speed); player.anims.play('right', true); }
  else { player.setVelocityX(0); player.anims.play('turn'); }
  if(doJump && player.body.touching.down) player.setVelocityY(-400);
  platforms.children.iterate(p=>{ if(p.x < player.x - config.width/2) p.destroy(); });
  this.coconuts.children.iterate(c=>{ if(c.x < player.x - config.width/2) c.destroy(); });
  scoreText.setText('Score: ' + score);
  this.cameras.main.startFollow(player, true, 0.05, 0.05);
}

function collect(player, coco) { coco.destroy(); score++; }
</script></body></html>
"""

st.components.v1.html(game_html, height=600)
