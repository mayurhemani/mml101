
Note: This is subject to revision

## Part 0. Recap of Deep Learning with a single modality (1 hour)

1. Deep learning features - vision, language
2. Attention and Transformers
3. Quiz 0
4. Vision Transformers

Outcome: An overview of the historical context of multimodal models

### Hands-on 0: (1.5 hours)
1. Nano GPT training on shakespeare dataset
2. Experiments with replacing the dataset with 2D curves

Outcome: A sense of autoregressive model training



## Part 1. Going multimodal (1 hour)
1. The *dimension analysis* of problems with Multimodal deep learning
2. Modality binding from first principles
3. Quiz 1: Modalities and Encodings for various problems.
4. The *prior* argument
	i. What you already know (the importance of pre-training)
	ii. What you can tell beforehand (the importance of additional input)

Outcome: An intuitive sense of what modalities are required for solving a problem.

### Hands-on 1: (1 hour)
1. OpenAI CLIP: Inference - zero-shot classification
2. LLaVA: Inference - image captioning

Outcome: Basic sense of two landmark papers



## Part 2. Alignment (1 hour)
1. Translation vs Alignment - equivalence classes in alignment
2. Emergence of similarity from comparisons
3. Quiz 2: Alignment problems for desired outcomes.
4. Search by content
	i. CLIP
	ii. HNSW

Outcome: A deep sense of what is happening in alignment-type multimodal models and related practical applications.

### Hands-on 2: (1 hour)
Building a complete search application with FAISS and CLIP.

Outcome: A good understanding of practical use of alignment-type multimodal models.



### Part 3. Co-processing modalities (1.5 hours)
1. Cross-attention and the backbone approach - the Perceiver model
2. Language models as the basis of unification – Image Captioning - (QFormer in BLIP2)
3. The Projection approach - LLaVA
4. Free-thinking session: new approaches to co-processing - Video case study

Outcome: A reasonable understanding of the techniques used in multimodality binding for neural networks.

### Hands-on 3: (1.5 hours)
Training a simple LLaVA model starting from NanoGPT and CLIP ViT.



## Part 4. Applications (1 hour)
1. Grounding and guard-rails
2. Text-is-all-you-Need (Visual programming e.g.)
3. "Agents"

Outcome: A sense of the problems when creating real-world applications, and current application-oriented thinking.

### Hands-on 4. (1.5 hour) 
Building a multimodal "agentic" system with Langgraph for marketing caption generation from images


