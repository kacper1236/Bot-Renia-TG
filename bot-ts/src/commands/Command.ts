import { Context } from "telegraf";

export class Command {
    constructor(public readonly name: string){}

    public async callback({telegram, message}: Context) {
        await telegram.sendMessage(message?.chat.id ?? '', "uwu :3 " + this.name);
    }
}