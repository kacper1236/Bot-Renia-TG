import 'dotenv/config'
import { Command } from "./commands";
import { Bot } from "./bot";
import { Action } from './actions';

const bot = new Bot();
const cmd = new Command('help');

bot.registerCommand(cmd);
bot.registerAction(new Action());

bot.run();