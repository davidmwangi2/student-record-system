import { useState, useEffect } from "react";
import BotList from "./components/BotList";
import YourArmy from "./components/YourArmy";
import BotService from "./services/BotService";

function App() {
  const [bots, setBots] = useState([]);
  const [army, setArmy] = useState([]);

  useEffect(() => {
    BotService.getBots().then(setBots);
  }, []);

  const enlistBot = (bot) => {
    if (!army.find((b) => b.id === bot.id)) {
      setArmy([...army, bot]);
    }
  };

  const releaseBot = (botId) => {
    setArmy(army.filter((bot) => bot.id !== botId));
  };

  const deleteBot = (botId) => {
    BotService.deleteBot(botId).then(() => {
      setBots(bots.filter((bot) => bot.id !== botId));
      setArmy(army.filter((bot) => bot.id !== botId));
    });
  };

  return (
    <div>
      <h1>Bot Battlr</h1>
      <YourArmy army={army} releaseBot={releaseBot} deleteBot={deleteBot} />
      <BotList bots={bots} enlistBot={enlistBot} deleteBot={deleteBot} />
    </div>
  );
}

export default App;