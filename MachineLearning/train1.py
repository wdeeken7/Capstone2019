from azureml.core import Workspace

try:
    ws = Workspace(subscription_id = "8402fd02-6a15-499c-bb04-1dee338962d6", resource_group = "NDSUCapstone2019", workspace_name = "Capstone2019MLServerWorksapce")
    # write the details of the workspace to a configuration file.
    ws.write_config()
    print("Workspace configuration succeeded. Skip the workspace creation steps below")
except:
    print("Workspace not accessible. Change your parameters or create a new workspace below")
dataset_root_azure = "https://capstone2019storage.table.core.windows.net/CleanedNormed20MeteStdDev"