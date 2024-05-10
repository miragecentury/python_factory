
# Install virtualenv and dependencies in it
poetry install --all-extras --with=test

# Install git cz tooling with the conventional-changelog
commitizen init --save-dev cz-conventional-changelog
