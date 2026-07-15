with open('taiwan-travel.html', encoding='utf-8') as f:
    html = f.read()

# Find renderTab food section
start = html.find("if(currentTab==='food')")
# Find the next section
end = html.find("if(currentTab", start + 20)
section = html[start:end]
print(f'Food section length: {len(section)} chars')

# Check for issues
backticks = section.count('`')
print(f'Backticks: {backticks} (should be even)')

# Check if there's a duplicate renderTab
count = html.count('function renderTab')
print(f'renderTab defined {count} times')

# Check selectCounty - does it set currentTab to food?
idx = html.find('function selectCounty')
print(f'selectCounty at char {idx}')
print(html[idx:idx+300])
