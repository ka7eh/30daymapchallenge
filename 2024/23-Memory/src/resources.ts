import { ImageFiltering, ImageSource, Loader, Resource } from 'excalibur';
import { TiledResource } from '@excaliburjs/plugin-tiled';

import { Player } from './player';

import backgroundPath from '../tiles/background.png?url';
import catPath from '../tiles/cat.png?url';
import tmxPath from '../tiles/liveeo.tmx?url';
import tilesetPath from '../tiles/Office_Furniture_01.png?url';
import tsxPath from '../tiles/Office_Furniture_01.tsx?url';

export const Resources = {
    HeroSpriteSheetPng: new ImageSource(catPath, false, ImageFiltering.Pixel),
    TiledMap: new TiledResource(tmxPath, {
        entityClassNameFactories: {
            player: (props) => {
                const player = new Player(props.worldPos);
                player.z = 100;
                return player;
            }
        },
        pathMap: [
            { path: 'liveeo.tmx', output: tmxPath },
            { path: 'Office_Furniture_01.png', output: tilesetPath },
            { path: 'Office_Furniture_01.tsx', output: tsxPath },
            { path: 'background.png', output: backgroundPath }
        ]
    }),
    TsxResource: new Resource(tsxPath, 'text')
};

export const loader = new Loader();
for (let resource of Object.values(Resources)) {
    loader.addResource(resource);
}
