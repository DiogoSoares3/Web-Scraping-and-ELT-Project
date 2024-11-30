uvicorn api.main:app --host 0.0.0.0 --port 8200 --reload &
streamlit run /app/ui/home.py --server.port 8210 --logger.level=debug --server.runOnSave true --theme.base dark
