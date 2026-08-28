# Pelota de Medias

**Pelota de Medias** is an open-source app for soccer fans. It begins with the Argentina men’s national team: a simple way to browse the match archive, find a day with a game, and eventually open a rich match center with lineups, formations, events, and statistics.

## The name

*Pelota de medias* is the improvised ball made by rolling one old sock inside another, then another, until there is something to play with. It is a small act of invention: football exists before the perfect pitch, equipment, or budget.

That is the spirit of this project. Start close to the game, make the useful thing, and grow it in the open.

## The logo

The logo is called **Pelota de Medias**. It should feel like a hand-rolled football: layered, imperfect, energetic, and unmistakably made for play. It is not a polished tournament ball; it is the ball you make when the only thing you need is a match.

## Current direction

The first release is focused on Argentina’s senior men’s national team:

- a calendar that highlights days with matches;
- a day view with that day’s results; and
- a match center for score, timeline, lineups, formations, team statistics, and player statistics when available.

The repository currently contains the local Docker prototype and its supporting collector/database code. The user interface and the data model are being designed first; live data collection will be added only when its source and use are appropriate.

## Run locally

```bash
docker compose up --build
```

Open [http://localhost:6001](http://localhost:6001).

## License

Pelota de Medias is licensed under the [GNU Affero General Public License v3.0](LICENSE). If you run a modified version for other people over a network, the AGPL requires you to offer them the corresponding source code.
