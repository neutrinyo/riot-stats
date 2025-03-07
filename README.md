# riot-stats
Work in progress.
App for visualization and statistical analysis of League of Legends match data fetched from Riot Games' API.
Built primarily with FastAPI and SQLAlchemy with the help of @iann838's Pulsefire library for Riot API related functionality.

## Planned functionality:
- fetching and storing selected match data in a PostgreSQL database (match metadata with positional info - champion kills and deaths)
- statistical analysis based on champion, role (eg. the average position of deaths based on role)
- kill/death heatmap sorted by side, position (currently planning to use the Plotly library, may be subject to change)
