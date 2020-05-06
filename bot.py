from telegram.ext import CommandHandler, Updater
import telegram
from data import get_data,get_creds
from googleapiclient.discovery import build

SAMPLE_SPREADSHEET_ID = '1sgGS9t7PaJpSmvw__DgSpumvr0hbaIGf0rhhvZYWXXI'

def query(data,col,value):
    for row in data:
        if row[col] == value:
            return data.index(row)
        else:
            pass


class Bot(object):

    def __init__(self):
        pass

    def ajuda(self,update,context):
        print('ajuda')
        response_message = "Para cadastro: /cadastro,\nPara ajuda: /ajuda\nPara mudar estado: /ocupado para ficar ocupado e /livre para ficar livre"
        update.message.reply_text(response_message)
                        
    def ocupado(self,update,context):
        print('ocupado')
        creds = get_creds()
        dados_voluntarios = get_data()
        username = update.message.from_user.username
        idx = query(dados_voluntarios,-2,username)
        service = build('sheets', 'v4', credentials=creds)
        value = [['Ocupado']]
        body = {'values': value}
        result = service.spreadsheets().values().update(
            spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Voluntarios!J%i'%(idx+2), 
            valueInputOption = 'RAW', body=body).execute()
        print('{} cells updated.'.format(result.get('updatedCells')))
        response_message = "Voluntário @{} passou para ocupado".format(username)
        update.message.reply_text(response_message)
        
    def livre(self,update,context):
        print('livre')
        creds = get_creds()
        dados_voluntarios = get_data()
        username = update.message.from_user.username
        idx = query(dados_voluntarios,-2,username)
        service = build('sheets', 'v4', credentials=creds)
        value = [['Disponível']]
        body = {'values': value}
        result = service.spreadsheets().values().update(
            spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Voluntarios!J%i'%(idx+2), 
            valueInputOption = 'RAW', body=body).execute()
        print('{} cells updated.'.format(result.get('updatedCells')))
        response_message = "Voluntário @{} passou para disponível.".format(username)
        update.message.reply_text(response_message)

    
def main():
    
    token = '1191656019:AAEOlPPJw9mILVQ_4Otmy2ttrFeWB5hxMBg'
    bot_vol = Bot()
    updater = Updater(token, use_context=True)
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    # on different commands - answer in Telegram
    dispatcher.add_handler(
        CommandHandler('ajuda', bot_vol.ajuda, pass_chat_data=True)
    )
    dispatcher.add_handler(
        CommandHandler('ocupado', bot_vol.ocupado, pass_chat_data=True)
    )
    dispatcher.add_handler(
        CommandHandler('livre', bot_vol.livre, pass_chat_data=True)
    )

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == "__main__":
    print("press CTRL + C to cancel.")
    main()