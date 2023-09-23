# dAIgram

dAIgram helps you grasp difficult concepts by transforming them into diagrams. Under the hood we use an AI model to generate Kroki diagrams. The main contribution of this work is ease of use and carefully designed prompts.

usage 
1. Clone repository
2. Export your OpenAI API credentials as environment variables
```
export OPENAI_API_KEY=YOUR_API_KEY
export OPENAI_API_ORG=YOUR_ORG_KEY
```
3. Create a prompt and save it as input.txt
4. run 
```
python main.py -m gpt-4 -n 3 input.txt -o diagrams
```

Where: 
- -m is the model version. Currently gpt-4, gpt-4-32k, gpt-3.5-turbo, gpt-3.5-turbo-16k are valid model versions
- -n is the number of diagrams you want to create 
- -o is the output directory

Examples of diagrams generated using gpt-4 (best of 3 generations): 

Prompt: 

*A comprehensive process flowchart outlining the steps involved in ordering a pizza from a traditional pizzeria. Customers place an order by calling the pizzeria or using their website. The order details, including pizza type, size, and delivery address, are recorded. The order is then transmitted to the kitchen staff. In the kitchen, chefs prepare the pizza with the requested toppings and sauces. The prepared pizza is then placed in a preheated oven for the specified cooking time. Once baked to perfection, the pizza is removed from the oven. If it's a delivery order, the pizza is dispatched to the customer's address by a delivery driver. The customer receives the pizza, completes the payment, and enjoys their meal.*

Result: 
![[pizza_example/diagram.svg]]

1. Pizza preparation by gpt-4

Prompt: 

*A detailed Venn diagram depicting the nuanced relationship between cats and dogs as pets. In the diagram, Circle A represents Cats with unique characteristics like Independence, Purring, and Agility. Circle B represents Dogs with unique characteristics like Loyalty, Energetic behavior, and Barking. The overlapping area illustrates Shared Traits and Benefits as Pets, such as Providing Companionship and Requiring Care and Attention.*

![[pet_example/diagram.svg]]
2. Common traits by gpt-4

**Warning: Only tested in gpt-4. I tried on on gpt-3.5-turbo but could not get it to work.**
