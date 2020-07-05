def munin_safe_id(id):
    return str(id).replace('.', '_').replace('/', '_')
