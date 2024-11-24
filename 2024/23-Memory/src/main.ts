import * as ex from 'excalibur';

import tilesetPath from '../tiles/liveeo_logo.png?url';
import { Resources, loader } from './resources';

loader.loadingBarColor = ex.Color.Black;
loader.loadingBarPosition = ex.vec(170, 470);
loader.playButtonText = "Let's Explore LiveEO";
loader.backgroundColor = ex.Color.White.toString();
loader.logo = tilesetPath;
loader.logoPosition = ex.vec(320, 180);

const game = new ex.Engine({
  width: 800,
  height: 600,
  canvasElementId: 'game',
  pixelArt: true,
  pixelRatio: 2
});
// game.toggleDebug();


game.start(loader).then(() => {
  Resources.TiledMap.addToScene(game.currentScene);
});
