# How to contribute to Vector AI?

Everyone is welcome to contribute, and we value everybody's contribution. Code
is thus not the only way to help the community. Answering questions, helping
others, reaching out and improving the documentations are immensely valuable to
the community.

It also helps us if you spread the word: reference the library from blog posts
on the awesome projects it made possible, shout out on Twitter/Reddit/Kaggle 
every time it has helped you, or simply star the repo to say "thank you".

## You can contribute in so many ways!

There are 4 ways you can contribute to Vector AI:
* Fix outstanding issues with the existing code;
* Suggest new ways to improve current Vector methodologies.
* Contribute to examples/new data notebooks!
* Submitting issues related to bugs or desired new features.

**All are equally valuable to the community!**

## Reporting A Bug

We would really appreciate it if you could **make sure the bug was not
already reported** (use the search bar on Github under Issues).

Did not find it? :( So we can act quickly on it, please follow these steps:

* Include your **OS type and version**;
* A short, self-contained, code snippet that allows us to reproduce the bug in
  less than 30s;
* Provide the *full* traceback if an exception is raised.

To help with this, we have several utilities to allow you to easily re-produce bugs. 
These can be done using the following:

```
# Create 500 sample documnents to quickly feed into whatever function is required.
vi_client.create_sample_documents(500)

# Create vectors of length 500
vi_client.generate_vector(500)

```

### Did you have a new feature suggestion for Vector AI?

Please provide the following information:

* Short description of the model and link to the paper;
* Link to the implementation if it is open-source;
* Link to the model weights if they are available.

The best feature requests will provide:

1. Motivation first:
  * Is it related to a problem/frustration with the library? If so, please explain
    why. Providing a code snippet that demonstrates the problem is best.
  * Is it related to something you would need for a project? We'd love to hear
    about it!
  * Is it something you worked on and think could benefit the community?
    Awesome! Tell us what problem it solved for you.
2. Write a *full paragraph* describing the feature;
3. Provide a **code snippet** that demonstrates its future use;
4. In case this is related to a paper, please attach a link;
5. Attach any additional information (drawings, screenshots, etc.) you think may help.

If your issue is well written we're already 80% of the way there by the time you
post it.

### How To Make A Pull Request

We suggest the following method if you are interested in contributing code to Vector AI!

1. Fork the repository. 
2. Clone the forked repository. 
3. Create a new branch. 
4. Push changes to your repository. 
5. Change remote to this repository.
6. Create a PR to this public repository. 

For detailed instructions, , we recommend: [this detailed guide on making pull requests in open source projects](https://opensource.com/article/19/7/create-pull-request-github).

### Running Tests

- When you are running tests, ensure that you have environment variables USERNAME and API_KEY set and that you run the following command if you are running tests using the client. 

```
python3 -m pytest --use_client
```

Alternatively, if you are adding functions, please use the following so we can save on compute: 
```
python3 -m pytest
```

### Tests

Tests are incredibly important for our library to ensure that errors are fixed.
Our main method of testing is running the notebooks and ensuring that their results are still viable. Therefore, please
try to re-run the notebooks to ensure that your submission is not causing errors (which usually will not be the case!)


### Style guide

For documentation strings, `Vector AI` aims to follows the [google style](https://google.github.io/styleguide/pyguide.html) as closely as possible.
For internal attributes, we use _ in front of the name of the attribute. 
However, we will not reject PRs if they do not follow this style.

### Running Automated API creation

To run the automated APi creation, simply run:
```
python utils/automate_api.py
```

#### This guide was inspired by Transformers [transformers guide to contributing](https://github.com/huggingface/transformers/blob/master/CONTRIBUTING.md) which was influenced by Scikit-learn [scikit-learn guide to contributing](https://github.com/scikit-learn/scikit-learn/blob/master/CONTRIBUTING.md).
