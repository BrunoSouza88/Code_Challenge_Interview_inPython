from flask import Flask, request, jsonify

app = Flask(__name__)

contas = [
    {'numero': 12345, 'saldo': 1000, 'user': 'jorge', 'token': []},
    {'numero': 54321, 'saldo': 500, 'user': 'maria', 'token': []},
    {'numero': 98765, 'saldo': 2500, 'user': 'teresa', 'token': []},
]


@app.route('/', methods=['GET'])
def get_contas():
    return jsonify(contas)


@app.route('/contas', methods=['POST'])
def post_contas():
    data = request.get_json()
    numero = data.get('numero')
    saldo = data.get('saldo')
    user = data.get('user')

    if not numero or not saldo or not user:
        return 'É necessário fornecer número, saldo e usuário.', 400

    existing_account = next(
        (conta for conta in contas if conta['user'] == user), None)

    if existing_account:
        return 'Essa conta já está cadastrada.', 409

    contas.append(
        {'numero': numero, 'saldo': saldo, 'user': user, 'token': []})
    return '', 200


@app.route('/auth', methods=['POST'])
def post_auth():
    data = request.get_json()
    user = data.get('user')

    if not user:
        return 'É necessário fornecer o usuário.', 400

    account = next((conta for conta in contas if conta['user'] == user), None)

    if not account:
        return 'Conta não encontrada.', 404

    account['token'] = 'TOKEN'
    return 'Autenticado com sucesso.', 200


@app.route('/transfer', methods=['POST'])
def post_transfer():
    data = request.get_json()
    origem = data.get('origem')
    destino = data.get('destino')
    valor = data.get('valor')
    token = request.headers.get('authentication-headers')

    if not token:
        return 'Token não fornecido.', 401

    conta_origem = next(
        (conta for conta in contas if conta['numero'] == origem), None)

    if not conta_origem or conta_origem['token'] != token:
        return 'Token inválido.', 401

    conta_destino = next(
        (conta for conta in contas if conta['numero'] == destino), None)

    if not conta_destino:
        return 'Conta de destino não encontrada.', 404

    if conta_origem['saldo'] < valor:
        return 'Saldo insuficiente.', 400

    conta_origem['saldo'] -= valor
    conta_destino['saldo'] += valor

    return 'Transferência realizada com sucesso.', 200


if __name__ == '__main__':
    app.run(port=4000)
