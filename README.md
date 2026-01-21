# Ligue 1 Match Prediction & Visualization
Data analysis and prediction project using automated data collection, feature engineering and machine learning to predict Ligue 1 match outcomes.

## Overview
This project combines automated data collection, feature engineering and machine learning to analyze Ligue 1 matches and estimate probabilistic outcomes for upcoming games.
### Automatic data collection
The data is automatically collected every monday morning from the Football-Data API.
### Feature engineering
For data visualization and prediction purpose, the following features are calculated:
- Classic performance features derived from league standings, such as rank, average goals scored and conceded, recent form (last 5 games), and win/loss rates.
-The ELOs. [ELO](https://en.wikipedia.org/wiki/World_Football_Elo_Ratings) is a ranking system. In this project, we don't use some official ELO ranking but an homemade ranking.
The ELO history is build using season 2023-2024 and 2024-2025 and extended on the current season (2025-2026). Before the start of the first season ELOs are initialized following a linear relationship to the team's ranking at the end of the previous season. Then for each season, the elos before the first matchday are calculated as a balance between the ELO at the end of previous season and 1500 which is usually considered the "baseline ELO". Then for each match played, the team who wins "takes" some ELO points from the losing team depending on their ELO difference and the number of goals scored. Team ELOs usually stabilize quickly at the start of a season, undergoing variations if the team goes through a bad or a good phase.


### Prediction Model
The project uses a Gradient Boosting classifier (scikit-learn) to estimate the probabilities of three match outcomes:
- HOME_TEAM
- DRAW
- AWAY_TEAM

The focus is on probabilistic outputs rather than hard predictions, as probabilities provide more nuanced information than a single predicted class.

The model relies on the following features:
- home_avg_goals_against: average goals conceded by the home team so far
- home_home_loss_rate: proportion of home games lost by the home team
- home_form_last5: points earned by the home team over the last 5 matches
- away_avg_goals_for: average goals scored by the away team
- away_form_last5: points earned by the away team over the last 5 matches
- dif_loss_rate: difference between both teams’ loss rates
- dif_elo_before: ELO difference before the match
- away_elo_before: away team ELO before the match

### Recurring pipeline
A weekly pipeline automatically updates match data, standings, ELO ratings and predictions. The pipeline is scheduled to run every Monday morning.
Limits: if there is two gamedays in a week (example on a wednesday) then I need to manually run the pipeline or there'd be a big problem. Additionally, if there is a delayed game like interruption or weather-delayed, it would probably cause a lot of problems. I have not handled these cases yet.

### Visualization
The [Streamlit app](https://ligue1viz-d4bj8ibdxppr7nmeks7dqn.streamlit.app/) is the main product of this project: a little visualization tool with two pages. 
The first page allows to compare the results of two teams very quickly: ranking evolution, total points, results in all the previous gamedays, cumulated goals for, cumulated goals against and goal average.
The second page shows the probability of outcomes for each of the 9 matchs in the next gameday.

## Motivation
I've been intersted in football for a long time. As a student, I did some predictions on my machine locally. I would type the gameday results in a spreadsheet to be able to do statistics on it. They included data visualization oppposing two teams who would next play against each other, prediction of the next matchday, and closer to the end of a season, predicting the end of the season using Monte Carlo methods to estimates the chances of a particular team finishing at different ranks. 
These ideas were great but deserved more than a little project locally: I decided to automate the data extraction and collection, perhaps do more complex models, and also make the reuslts available to friends.
An additional goal was to gain new skills, like Streamlit, and 'train' in others with real-world data: applying Machine Learning models, try my hand at some basic data engineering.

## Project architecture
data/
├── raw/          # raw data from the API
├── processed/    # processed data for the app and pipelines
app/              # streamlit app
├── pages/        # the two pages for the app
models/           # the saved model for prediction
notebooks/        # Were used in the developpement of this project. explore is just a tool, prediction details the model selection
src/
├── api/          # link to the API
├── etl/          # data extraction & transformation
├── features/     # feature engineering
├── pipeline/     # scheduled weekly pipeline, pieplien to build initial elo history, and the model training pipeline
├── viz/          # some visualisation functions to be used in the app (plots...)

## Technical choices
- Python, pandas, scikit-learn
- Gradient Boosting chosen for its robustness on tabular data
- Probability calibration to improve probabilistic outputs
- Parquet format used for intermediate datasets

## Roadmap / Next steps
-I could include a Monte-Carlo + prediction model based end of season prediction. The limits of that idea: the model used can't include any 'goal related' stats (that includes ELO) so it needs to be very simple thus pretty naive.
I shoudl find a way to handle the "two gamedays in a week" / delayed matchday situation

## Disclaimer
This is a personnal project made 'for fun' but made available for other fans. It is NOT intended to help anyone in betting games. betting apps ave way better models and this is not going to beat them. Betting is dangerous and you should do it at your own risks.