import argparse, sys
from training_data import * 
from decouple import config, UndefinedValueError

if __name__ == '__main__':

    def main():
        parser = argparse.ArgumentParser(description="Run the process to get and transform the training data for the model")
        parser.add_argument("-G", "--get_data", help="Run the process to obtain the training data from the database", nargs=3)
        parser.add_argument("-E", "--encrypt_conn_str", help="Run the process to encrypt connection str to the database", nargs=2)

        args = vars(parser.parse_args())
        #usage: main.py "-G" "C:\Users\USER\Documents\my files\ml_interview\db_folder\config.json" "reddit_usernames" "reddit_usernames_comments"
        if args["get_data"] is not None:
            print("Data extraction has started")
            config_filepath = args["get_data"][0]
            usernames_table_name = args["get_data"][1]
            users_comments_table_name = args["get_data"][2]
            try:
                key = config('SECRET_KEY')
            except UndefinedValueError:
                sys.exit(f"SECRET_KEY is not defined. Kindly use a .env file or set it on the command line. set SECRET_KEY=temporary_value")

            data_processor = DataProcessor(key,config_filepath)
            data_processor.get_data(usernames_table_name, users_comments_table_name)

        elif args["encrypt_conn_str"] is not None:
            try:
                key = config('SECRET_KEY')
            except UndefinedValueError:
                sys.exit(f"SECRET_KEY is not defined. Kindly use a .env file or set it on the command line.")
                
            print("Data encryption has started")
            config_filepath = args["encrypt_conn_str"][0]
            string_to_encrypt = args["encrypt_conn_str"][1]
            encryptor = AESCipher(key)
            # Encrypt a string
            encrypted_string = encryptor.encrypt(string_to_encrypt)
            encryptor.save_to_json(encrypted_string, config_filepath)

    main()