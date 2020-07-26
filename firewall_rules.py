import googleapiclient.discovery

compute = googleapiclient.discovery.build('compute', 'v1', cache_discovery=False)

def main(request):
    """Activate/deactivate firewall rules
    """

    project = request.args.get('project')
    rules = request.args.getlist('rules', type=int)

    messages = []
    for rule_id in rules:
      # get current state
      rule_status = compute.firewalls().get(project=project,
                                            firewall=str(rule_id)).execute()
      enabled = rule_status['disabled']

      # decide action
      if enabled:
        request_body = {'disabled' : False}
        echo = 'enabled'
      else:
        request_body = {'disabled' : True}
        echo = 'disabled'
      
      # toggle state
      compute.firewalls().patch(project=project,
                               firewall=str(rule_id),
                               body=request_body).execute()

      # print action
      messages.append("Rule {} was {}".format(rule_status['name'], echo))
    
    output = "\n".join(messages)
    headers = {'Content-Type': 'text/plain; charset=utf-8'}

    return output, headers


