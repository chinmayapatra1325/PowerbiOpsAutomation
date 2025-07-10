# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   }
# META }

# MARKDOWN ********************

# ### Fabric Data Agent Automation Library

# MARKDOWN ********************

# ### Introduction
# This notebook demonstrates how to automate Fabric data agent functionalities such as creating a data agent; adding a datasource (e.g. Lakehouse) or adding instructions to a data agent programmatically using our library. More information on data agent can be found [here](https://learn.microsoft.com/en-us/fabric/data-science/concept-ai-skill).

# CELL ********************

%pip install fabric-data-agent-sdk

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from fabric.dataagent.client import (
    FabricDataAgentManagement,
    create_data_agent,
    delete_data_agent,
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# First, let's create a data agent

# CELL ********************

data_agent_name = "data_agent_automation_sample"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# create DataAgent
data_agent = create_data_agent(data_agent_name)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# You can check the configuration of a data agent as shown below

# CELL ********************

# by default the instructions and description for the data agent will be empty, we will update them later in the notebook
data_agent.get_configuration()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# You can also initialize a client for an existing data agent

# CELL ********************

data_agent = FabricDataAgentManagement(data_agent_name)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# Update data agent with instructions and a description

# CELL ********************

data_agent.update_configuration(
    instructions="You are a helpful assistant, help users with their questions",
    user_description="Data agent to assists users with insights from the AdventureWorks dataset.",
)
data_agent.get_configuration()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# You will now add a datasource to your data agent. In this sample, you will add a Lakehouse as a datasource, however you can also add Semantic Model or KQL database.
# 
# You will work with a sample Lakehouse called AdventureWorks for the remainder of the notebook, you can also create the same Lakehouse by following the instructions here: https://learn.microsoft.com/en-us/fabric/data-science/ai-skill-scenario#create-a-lakehouse-with-adventureworksdw
# 
# If you name your Lakehouse `AdventureWorks` the rest of the notebook should run without requiring any changes. If you would like to use your own Lakehouse, make sure to change the `lakehouse_name` and other relevant variables throughout the notebook.

# CELL ********************

# add a lakehouse
lakehouse_name = "AdventureWorks"
# datasource type could be: lakehouse, kqldatabase, datawarehouse or semanticmodel
data_agent.add_datasource(lakehouse_name, type="lakehouse")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# we can check which datasources are added to the data agent
data_agent.get_datasources()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# You can publish the data agent.

# CELL ********************

data_agent.publish()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# Now you will work with the datasource you just added.

# CELL ********************

datasource = data_agent.get_datasources()[0]

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# You can take a look at the tables and the columns in the datasource. 
# 
# - Note that by default, the datasource is initialized with no table selected. A `*` next to the table indicates selected table.
# - You can select tables using `datasource.select` to pick the right tables or all tables related to the context of the question.
# - Selecting a table will also select all columns in the table.

# CELL ********************

datasource.pretty_print()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# You can add/remove table to consider/not consider them in query generation.

# CELL ********************

datasource.select("dbo", "dimcurrency")
datasource.select("dbo", "dimemployee")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# You will see that the `*` will appear next to the `dimcurrency` and `dimemployee` tables, as they are now selected.

# CELL ********************

datasource.pretty_print()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# Now let's unselect the `dimcurrency` table.

# CELL ********************

datasource.unselect("dbo", "dimcurrency")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# You will notice from the missing `*` next to the columns under the `dimcurrency table`, now that you un-selected the table, which means the data agent is instructed to not use the un-selected table when generating an answer.

# CELL ********************

datasource.pretty_print()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# You can also add few-shot examples.

# CELL ********************

example_question = "How many employees are there in the company?"
example_query = "SELECT COUNT(*) AS NumberOfEmployees FROM dbo.dimemployee"
example_fewshots = {example_question: example_query}
datasource.add_fewshots(example_fewshots)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

datasource.get_fewshots()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# You can delete few-shots using their ids.

# CELL ********************

# make sure the replace the id of the few-shot example with the id that is assigned to your few-shot example
datasource.remove_fewshot("03f6dc18-b372-4766-ad4e-f2d8c340da58")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

datasource.get_fewshots()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# Finally, we can delete the data agent

# CELL ********************

delete_data_agent(data_agent_name)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
