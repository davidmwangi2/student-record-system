function BotCard({ bot, enlistBot, deleteBot }) {
    return (
      <div className="bot-card" onClick={() => enlistBot(bot)}>
        <h3>{bot.name}</h3>
        <p>Class: {bot.class}</p>
        <button
          onClick={(e) => {
            e.stopPropagation();
            deleteBot(bot.id);
          }}
        >
          Delete
        </button>
      </div>
    );
  }
  
  export default BotCard;
npm  