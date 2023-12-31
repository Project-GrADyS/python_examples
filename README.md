# Gradys SIM Nextgen & GradysSimulations Examples

## Example types

This repo contains two types of examples:

- **Starter:** Runnable examples for others to use. 

- **Components:** Re-usable helper methods to use to create new **Starter**.

### Prerequisite: Installing Gradys SIM Nextgen

If this is the first time you're using Gradys SIM Nextgen, you first need to install the pip package. Use the following command:
- **Install Command**: `pip install gradysim`

## Starters

| Name                           | Description                                        |
|--------------------------------|----------------------------------------------------|
| [zigzag](zigzag)     | ZigZag Protocol                                  |

### Running Starters

Each sub-folder in this repo contains a runnable **Starter** example.

Execute the `main.py` to run the example.

For example, to run the zigzag example:

```bash
$ cd [path/to/examples/folder]/zigzag
$ python main.py
```

## Components

The [components](components) sub-folder contains reusable helper methods to create new **Starter**.

| Name                          | Description                                                                         |
|-------------------------------|-------------------------------------------------------------------------------------|
| [generator](components/generator) | Generate python and omnetpp examples based on a pattern |
| [statistic_visualizer](components/statistic_visualizer) | Python notebook to visualize the collected statistics of GradysNextGen and GradysSimulations|

## Contribute your templates

Contribute a example by submitting a Pull Request to the [Open Source Examples Repo](https://github.com/Project-GrADyS/examples): `https://github.com/Project-GrADyS/examples`




Different scenarios different uav, different amount of sensors 4, 8, 16
sensors 10, 20, 40

Graphs should have One single graph for each scenario
Average for all the runs 

run only omnet 