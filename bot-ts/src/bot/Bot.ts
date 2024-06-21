import { Telegraf } from "telegraf";
import { Command } from "../commands";
import { Action } from "../actions";

export class Bot {
    private instance: Telegraf;

    constructor(){
        const token = process.env['TG_TOKEN']!;

        this.instance = new Telegraf(token);
    }

    public registerCommand(cmd: Command) {
        this.instance.command(cmd.name, cmd.callback.bind(cmd));
    }

    public registerAction(action: Action){
        this.instance.on(action.filters, action.callback.bind(action))
    }

    public run(){
        this.instance.launch();

        // Enable graceful stop
        process.once('SIGINT', () => this.instance.stop('SIGINT'));
        process.once('SIGTERM', () => this.instance.stop('SIGTERM'));
    }
}