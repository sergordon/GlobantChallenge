import os
import logging
import pandas as pd

class LoggerManager:
    def __init__(self, log_dir="logs", log_file="app.log"):
        os.makedirs(log_dir, exist_ok=True)
        self.log_path = os.path.join(log_dir, log_file)

        # Usa un logger exclusivo basado en el nombre del archivo
        logger_name = log_file.replace(".log", "")
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)

        # Evita agregar múltiples handlers al mismo logger
        if not self.logger.handlers:
            file_handler = logging.FileHandler(self.log_path, mode='a')
            file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(file_handler)

            # (opcional) también loguea en consola
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(stream_handler)

    def log_error(self, message):
        self.logger.error(message)

    def log_info(self, message):
        self.logger.info(message)

    def log_dataframe(self, df: pd.DataFrame, filename="dataframe_log.csv"):
        filepath = os.path.join(os.path.dirname(self.log_path), filename)
        write_header = not os.path.exists(filepath)
        df.to_csv(filepath, mode='a', index=False, header=write_header)
        self.log_info(f"Logged DataFrame to {filename}")
