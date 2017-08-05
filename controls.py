import telepot
import emoji
import requests

def logs(msg, user):
    from datetime import datetime
    ct, chat_type, chat_id = telepot.glance(msg)
    now = datetime.now()
    msg1 = str(msg["text"])
    log = open("log1.txt", 'a')
    log.write("%s/%s/%s %s:%s ->>> Id: %s / User: @%s / Texto: %s\n" % (
    now.day, now.month, now.year, now.hour, now.minute, chat_id, user, msg1))
    log.close()

def start(text, chat_id, bot, user):
    if text == "/start":
        bot.sendMessage(chat_id, "Olá %s, bem-vindo ao BlockChain Bot!\n Digite /help para ver os comandos e opções." %user)

def transaction(text, chat_id, bot):
    if text.split()[0] == "/t":
        addr = text.split()[1]
        info_r = requests.get("https://api.blockcypher.com/v1/btc/main/txs/%s" %addr)
        info = info_r.json()
        adress_in = str(info["addresses"][1])  # Endereço de entrada
        adress_out = str(info["addresses"][0])  # enderesso de saída
        valor_r1 = float(info["total"]) * 10 ** -8  # Valor total --- OBS: *10**-8 Converte de satoshi para BTC
        fee1 = float(info["fees"]) * 10 ** -8  # taxas da transação
        valor_env = valor_r1 + fee1  # Valor total enviado (inclue taxas)
        receiv = str(info["received"])  # Data do recebimento
        conf = str(info["confirmations"])  # confirmações
        # Envia retorno ao User:
        bot.sendMessage(chat_id, emoji.emojize("Recebido em: %s\n\n :outbox_tray:Endereço de Saída: %s \n\n "
                                               ":inbox_tray:Endereço de Entrada: %s \n\n :money_with_wings:Valor enviado: %f btc\n\n "
                                               ":moneybag:Valor recebido: %f btc\n\n "
                                               ":small_red_triangle_down:Taxa: %f btc\n\n  :white_check_mark:Confirmações: %s\n\n\n "
                                               ":information_source:Informações por Blockcypher.com"
                                               %(receiv, adress_in, adress_out, valor_env, valor_r1, fee1, conf), use_aliases=True))
def wallet(text, chat_id, bot):
    if text.split()[0] == "/w":
        addr = text.split()[1]
        info_r = requests.get("https://api.blockcypher.com/v1/btc/main/addrs/%s" %addr)
        info = info_r.json()
        t_received = float(info["total_received"])*10**-8
        balance = float(info["balance"]) * 10 ** -8
        un_balance = float(info["unconfirmed_balance"]) * 10 ** -8
        n_trans = int(info["n_tx"])
        u_trans = int(info["unconfirmed_n_tx"])
        bot.sendMessage(chat_id, emoji.emojize(
            "Endereço: %s \n\n:moneybag: Saldo: %f btc \n\n:money_with_wings: Total Recebido: %f btc \n\n:white_circle: Saldo não confirmado: %f btc \n\n"
            ":white_check_mark: Nº de transações confirmadas: %d \n\n:x: Transações não confirmadas: %d" % (
            addr, balance, t_received, un_balance, n_trans, u_trans), use_aliases=True))

def fee(chat_id, bot, text):
    if text.split()[0] == "/fee":
        info_r = requests.get("https://bitcoinfees.21.co/api/v1/fees/recommended")
        info = info_r.json()
        fastest_fee = int(info["fastestFee"])
        halfHour_fee = int(info["halfHourFee"])
        hour_fee = int(info["hourFee"])
        try:
            out = int(text.split()[1])
            inp = int(text.split()[2])
            size = out * 34 + 180 * inp + 10
            fastest_fee1 = size * fastest_fee * 10 ** -8
            halfHour_fee1 = size * halfHour_fee * 10 ** -8
            hour_fee1 = size * hour_fee * 10 ** -8
            bot.sendMessage(chat_id, emoji.emojize("Sua transação está estimada em %d bytes\n\n:rocket: Taxa rápida: %f btc \n\n:bullettrain_side: Até 30min para confirmar: %f btc\n\n:turtle: Até 1h para confirmar: %f btc" %(size, fastest_fee1, halfHour_fee1, hour_fee1), use_aliases=True))
        except:
            bot.sendMessage(chat_id, emoji.emojize(":clock1: Taxa mais rápida: \n%d sts/byte\n\n:clock130: Confirma em cerca de 30 min: %d sts/byte\n\n:clock2: Confirma em cerca de 1h: \n%d sts/byte" %(fastest_fee, halfHour_fee, hour_fee), use_aliases=True))

def rate(text, bot, chat_id):
    if text.split()[0] == "/rate":
        if text.split()[1] == "brl" or text.split()[1] == "real" or text.split()[1] == "BRL":
            info_r = requests.get("https://www.mercadobitcoin.net/api/ticker/")
            info = info_r.json()
            rat = int(info["ticker"]["last"])
            alta = int(info["ticker"]["high"])
            baixa = int(info["ticker"]["low"])
            bot.sendMessage(chat_id, emoji.emojize(
                ":chart_with_upwards_trend: Alta: %d BRL\n:on: Atual: %d BRL\n:chart_with_downwards_trend: Baixa: %d BRL" % (
                alta, rat, baixa), use_aliases=True))
        elif text.split()[1] == "usd" or text.split()[1] == "dólar" or text.split()[1] == "USD":
            info_r = requests.get("http://api.coindesk.com/v1/bpi/currentprice.json")
            info = info_r.json()
            rat = info["bpi"]["USD"]["rate"]
            bot.sendMessage(chat_id, emoji.emojize(":dollar: Cotação Atual: %s USD" % rat, use_aliases=True))

        elif text.split()[1] == "eur" or text.split()[1] == "EUR" or text.split()[1] == "euro":
            info_r = requests.get("http://api.coindesk.com/v1/bpi/currentprice.json")
            info = info_r.json()
            rat = info["bpi"]["EUR"]["rate"]
            bot.sendMessage(chat_id, emoji.emojize(":euro: Cotação Atual: %s EUR" %rat, use_aliases=True))
        else:
            bot.sendMessage(chat_id, emoji.emojize(" :red_circle: Moeda inválida! Disponível apenas Euro, Real e Dólar.",
                                                   use_aliases=True))

def qr_code(text, bot, chat_id):
    if text.split()[0] == "/qr":
        addr = text.split()[1]
        bot.sendPhoto(chat_id, "https://api.qrserver.com/v1/create-qr-code/?size=460x320&data=%s" %addr)
