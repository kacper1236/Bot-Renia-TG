import { Context } from "telegraf";
import {Filter, message} from 'telegraf/filters';
import { Update } from "telegraf/typings/core/types/typegram";

export class Action {
    public get filters(): Filter<Update>  { // powalony typ
        return message('text');
    }

    public async callback({telegram, message}: Context) {
        await telegram.sendMessage(message?.chat.id ?? '', "owo :3 ");
    }

}