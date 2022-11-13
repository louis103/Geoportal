# Now, let’s say you will like to retrieve a list of your projects,
# having the most recently updated at the top. 
# To achieve this, you will 
# need to order the projects by updated_at in descending order. 
# See below how to do so:
# myprojects = Project.objects.order_by('-updated_at')
# Note the minus sign is indicating descending order. You could retrieve your project in ascending order as well, just removing the minus sign. See the example below:
# myprojects = Project.objects.order_by('updated_at')
# myprojects = Project.objects.order_by('title','color')
# myproject_list = Project.objects.filter(color='#000000')
# myproject_list = Project.objects.filter(color='#000000', title='My project')

#  We might want to retrieve any project that includes the word HTML within the description. Here is how you can do that:
# html_project_list = Project.objects.filter(description__icontains='html')
# Using __contains, you can indicate the filter should perform a contains operation.
# There are a few more operations available like startswith, endswith, lte(less than), gte(greater than), and range( equivalent to the between SQL operator).

# non_black_project_list = Project.objects.exclude(color='#000000')
# Note that you can combine the exclude method with a filter. For instance, you could retrieve any project that contains html in the description and is not black. See the code below:
# html_non_black_project_list = Project.objects.filter(description__icontains='html').exclude(color='#000000')

# You could also combine both operations .filter() and .order_by() and obtain a list of sorted entries that meet specific criteria. Following our project example, I could retrieve the projects with something to do with HTML, ordered by last time updated. The project that was updated most recently should be at the top, in other words, in descending order. See below the code to achieve that:
# html_project_list = Project.objects.filter(description__icontains='html').order_by('-updated_at')

# For instance, in our project example we could need to retrieve a project with an specific title. See how to do this below:
# searched_project = Project.objects.get(title='My project')