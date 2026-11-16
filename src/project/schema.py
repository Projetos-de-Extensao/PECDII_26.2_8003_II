def apenas_rotas_da_api(endpoints, **kwargs):
    # o app.urls tambem esta montado na raiz; documentamos so o prefixo /api/
    return [e for e in endpoints if e[0].startswith('/api/')]
