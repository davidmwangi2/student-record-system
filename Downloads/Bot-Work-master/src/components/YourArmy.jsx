import BotCard from "./BotCard";
function YourArmy({ army, releaseBot, deleteBot }) {
  return (
    <div>
      <h2>Your Army</h2>
      <div className="bot-container">
        {army.map((bot) => (
          <BotCard key={bot.id} bot={bot} enlistBot={() => releaseBot(bot.id)} deleteBot={deleteBot} />
        ))}
      </div>
    </div>
  );
}

export default YourArmy;