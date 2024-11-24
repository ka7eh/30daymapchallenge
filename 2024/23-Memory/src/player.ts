import * as ex from 'excalibur';
import { Resources } from './resources';
import { Config } from './config';

export class Player extends ex.Actor {
    constructor(pos: ex.Vector) {
        super({
            pos,
            width: 32,
            height: 32,
            collisionType: ex.CollisionType.Active
        })
    }

    onInitialize(game: ex.Engine): void {
        game.currentScene.camera.strategy.lockToActor(this);

        const playerSpriteSheet = ex.SpriteSheet.fromImageSource({
            image: Resources.HeroSpriteSheetPng as ex.ImageSource,
            grid: {
                spriteWidth: 32,
                spriteHeight: 32,
                rows: 18,
                columns: 18
            }
        });

        const idle = new ex.Animation({
            frames: [
                { graphic: playerSpriteSheet.getSprite(4, 1) as ex.Sprite, duration: Config.PlayerFrameSpeed },
                { graphic: playerSpriteSheet.getSprite(5, 1) as ex.Sprite, duration: Config.PlayerFrameSpeed },
                { graphic: playerSpriteSheet.getSprite(6, 1) as ex.Sprite, duration: Config.PlayerFrameSpeed },
                { graphic: playerSpriteSheet.getSprite(7, 1) as ex.Sprite, duration: Config.PlayerFrameSpeed },
                { graphic: playerSpriteSheet.getSprite(4, 2) as ex.Sprite, duration: Config.PlayerFrameSpeed },
                { graphic: playerSpriteSheet.getSprite(7, 1) as ex.Sprite, duration: Config.PlayerFrameSpeed },
                { graphic: playerSpriteSheet.getSprite(6, 1) as ex.Sprite, duration: Config.PlayerFrameSpeed },
                { graphic: playerSpriteSheet.getSprite(5, 1) as ex.Sprite, duration: Config.PlayerFrameSpeed },
            ]
        })
        this.graphics.add('idle', idle);

        const leftWalk = new ex.Animation({
            frames: [
                { graphic: playerSpriteSheet.getSprite(12, 3) as ex.Sprite, duration: Config.PlayerFrameSpeed },
                { graphic: playerSpriteSheet.getSprite(13, 3) as ex.Sprite, duration: Config.PlayerFrameSpeed },
                { graphic: playerSpriteSheet.getSprite(14, 3) as ex.Sprite, duration: Config.PlayerFrameSpeed },
                { graphic: playerSpriteSheet.getSprite(15, 3) as ex.Sprite, duration: Config.PlayerFrameSpeed },
            ]
        })
        this.graphics.add('left-walk', leftWalk);

        const rightWalk = new ex.Animation({
            frames: [
                { graphic: playerSpriteSheet.getSprite(12, 15) as ex.Sprite, duration: Config.PlayerFrameSpeed },
                { graphic: playerSpriteSheet.getSprite(13, 15) as ex.Sprite, duration: Config.PlayerFrameSpeed },
                { graphic: playerSpriteSheet.getSprite(14, 15) as ex.Sprite, duration: Config.PlayerFrameSpeed },
                { graphic: playerSpriteSheet.getSprite(15, 15) as ex.Sprite, duration: Config.PlayerFrameSpeed },
            ]
        });
        this.graphics.add('right-walk', rightWalk);

        const upWalk = new ex.Animation({
            frames: [
                { graphic: playerSpriteSheet.getSprite(12, 9) as ex.Sprite, duration: Config.PlayerFrameSpeed },
                { graphic: playerSpriteSheet.getSprite(13, 9) as ex.Sprite, duration: Config.PlayerFrameSpeed },
                { graphic: playerSpriteSheet.getSprite(14, 9) as ex.Sprite, duration: Config.PlayerFrameSpeed },
                { graphic: playerSpriteSheet.getSprite(15, 9) as ex.Sprite, duration: Config.PlayerFrameSpeed },
            ]
        });
        this.graphics.add('up-walk', upWalk);

        const downWalk = new ex.Animation({
            frames: [
                { graphic: playerSpriteSheet.getSprite(12, 1) as ex.Sprite, duration: Config.PlayerFrameSpeed },
                { graphic: playerSpriteSheet.getSprite(13, 1) as ex.Sprite, duration: Config.PlayerFrameSpeed },
                { graphic: playerSpriteSheet.getSprite(14, 1) as ex.Sprite, duration: Config.PlayerFrameSpeed },
                { graphic: playerSpriteSheet.getSprite(15, 1) as ex.Sprite, duration: Config.PlayerFrameSpeed },
            ]
        });
        this.graphics.add('down-walk', downWalk);
    }

    onPreUpdate(engine: ex.Engine): void {
        this.vel = ex.Vector.Zero;

        this.graphics.use('idle');
        if (engine.input.keyboard.isHeld(ex.Keys.ArrowRight)) {
            this.vel = ex.vec(Config.PlayerSpeed, 0);
            this.graphics.use('right-walk');
        }
        if (engine.input.keyboard.isHeld(ex.Keys.ArrowLeft)) {
            this.vel = ex.vec(-Config.PlayerSpeed, 0);
            this.graphics.use('left-walk');
        }
        if (engine.input.keyboard.isHeld(ex.Keys.ArrowUp)) {
            this.vel = ex.vec(0, -Config.PlayerSpeed);
            this.graphics.use('up-walk');
        }
        if (engine.input.keyboard.isHeld(ex.Keys.ArrowDown)) {
            this.vel = ex.vec(0, Config.PlayerSpeed);
            this.graphics.use('down-walk');
        }

    }
}
