# AI-chat-interface-for-DataSpell-Data-Analysis-IDE-
An app solving this task:
Let's remind us of the two layers of abstraction we want to introduce:
1) Set of pre-defined commands for manipulating data, visualisation etc.
2) AI chat for generating sequences of such commands based on user input.

While you're suggested to care only about the second layer on the internship, in this test assignment we propose you to implement both, but in a small and toy manner.
Thus, the task is to start with a very restricted set of data transformations over a pandas dataframe, for example, filter by predicate and selecting some columns. Then make an LLM-based script which will generate a sequence of such transformations. You can either use an open-source LLM or write us to get a token to access an OpenAI model. And finally, the sequence should be applied to the dataframe. We suggest that you consider the following:

Think about the structure of a transformation.
Use some tools which are enabling to ask LLM to generate a structured output to ensure correctness of the transformations’ sequence. (LangChain or others)
For local running LLMs you could use Cadence plugin if your laptop isn't sufficient enough.
Try to implement the solution as a project with Python files, not as a notebook.
