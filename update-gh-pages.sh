# Based on http://sleepycoders.blogspot.cz/2013/03/sharing-travis-ci-generated-files.html

if [ "$TRAVIS_PULL_REQUEST" == "false" ]; then
  echo -e "Starting to update gh-pages\n"

  # copy data we're interested in to other place
  cp -R cover $HOME/cover

  # go to home and setup git
  cd $HOME
  git config --global user.email "travis@travis-ci.org"
  git config --global user.name "Travis"

  # using token clone gh-pages branch
  git clone --quiet --branch=gh-pages https://${GH_TOKEN}@github.com:Ishino/batoru-royale.git gh-pages > /dev/null

  # go into directory and copy data we're interested in to that directory
  cd gh-pages
  cp -Rf $HOME/cover/* ./cover

  # add, commit and push files
  git add -f .
  git commit -m "Travis build $TRAVIS_BUILD_NUMBER coverage report pushed to gh-pages"
  git push -fq origin gh-pages > /dev/null

  echo -e "Pushed coverage report to Github Pages: http://ishino.github.io/batoru-royale/cover/\n"
fi