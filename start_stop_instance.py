import googleapiclient.discovery

compute = googleapiclient.discovery.build('compute', 'v1', cache_discovery=False)

def main(request):
    """Toggles compute engine instance start-stop
    """

    project = request.args.get('project')
    zone = request.args.get('zone')
    instance_name = request.args.get('instance')

    # get current state
    instance = compute.instances().get(project=project,
                                zone=zone,
                                instance=instance_name).execute()

    # decide command
    if instance['status'] == "TERMINATED":
        compute.instances().start(project=project,
                                zone=zone,
                                instance=instance_name).execute()

        return "{} turned on".format(instance_name)
    else:
        compute.instances().stop(project=project,
                                zone=zone,
                                instance=instance_name).execute()
        
        return "{} turned off".format(instance_name)


