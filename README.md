# "YouTube Data Analyzer: Unveiling Insights from Social Media Channels"

## Project Overview:
The "YouTube Data Analyzer" is a comprehensive tool designed to retrieve, analyze, and store data from multiple YouTube channels. It offers a user-friendly Streamlit interface that empowers users to make data-driven decisions, refine content strategies, and stay competitive in the dynamic world of social media.

## Table of Contents
1. [Features](#features)
2. [Getting Started](#getting-started)
3. [Prerequisites](#Prerequisites)
4. [Installation](#Installation)
5. [Usage](#Usage)
6. [Data Flow](#Data-Flow)
7. [Business Values](#Business-Values)
8. [Contributing](#Contributing)
9. [License](#License)
10. [Author](#Author)

## Features
**YouTube Data Retrieval:** Collect channel details, video information, likes, dislikes, comments, and more using the Google API.
**MongoDB Data Lake:** Store collected data in a MongoDB database, allowing for efficient storage of unstructured and semi-structured data.
**SQL Data Warehouse:** Migrate data to a SQL database, facilitating structured data analysis and reporting.
**Streamlit Interface:** Intuitive user interface for data access, visualization, and SQL query execution.
**Insightful SQL Queries:** Perform a wide range of SQL queries to extract valuable insights from the data.

## Getting Started
These instructions will help you set up and run the "YouTube Data Analyzer" project on your local machine for development and testing purposes.

## Prerequisites
Before running the project, ensure you have the following prerequisites installed:

* Python 3
* MongoDB
* [SQL Database (e.g., MySQL, PostgreSQL)]
* Streamlit
* Google API Key

## Installation
1.Clone the GitHub repository.
2.Install project dependencies(view requirements.txt file).
3.Configure API keys and database connections.
4.Run the Streamlit app.

## Usage
* Enter the YouTube channel IDs to retrieve data.
* Click the "Store Data" button to save data in MongoDB.
* Select channels to migrate to SQL tables.
* Execute SQL queries to extract valuable insights.
* Explore the Streamlit app for data visualization and analysis.

## Data Flow
Data Flow
The "YouTube Data Analyzer" project involves a unstructured data flow that encompasses data retrieval, storage, and analysis. Here's how data flows through the system:

#### User Interaction:
* Users input YouTube channel IDs into the Streamlit interface to request data retrieval.
* Clicking the "Store Data" button triggers the collection of data from the YouTube API.

#### Data Retrieval:
* The project utilizes the Google API to retrieve relevant data, including channel details, video information, likes, dislikes, comments, and more.
* Retrieved data is unstructured/structured in JSON format.

#### MongoDB Data Lake:
* The collected data is stored in a MongoDB database, which serves as a data lake. MongoDB excels at handling unstructured and semi-structured data, making it a suitable choice for this purpose.

#### SQL Data Warehouse:
* Users can select specific channels and migrate their data from the MongoDB data lake to a SQL database, such as MySQL or PostgreSQL.
* Data migration to SQL facilitates structured data analysis and reporting.

#### SQL Query Execution:
* SQL queries, stored in the sql_queries directory, are executed to extract insights from the migrated data. These queries address a range of data analysis tasks.
* Users can execute SQL queries directly through the Streamlit app.

#### Streamlit Interface:
* The user-friendly Streamlit interface provides access to the stored data, enabling visualization, analysis, and interaction with the dataset.
* Users can explore charts, graphs, and tables that offer insights into YouTube channel and video performance.
* The data flow in the "YouTube Data Analyzer" project follows a systematic path, from user interaction to data retrieval, storage in MongoDB, migration to SQL, SQL query execution, and finally, presentation through the Streamlit interface.

This textual description of the data flow provides an overview of how data moves through your project without relying on images or diagrams.

## Business Values
Various businesses and individuals can leverage the "YouTube Data Analyzer" project to gain valuable insights and improve their strategies on the YouTube platform. Here are some examples of how different entities can benefit from this project:

#### Content Creators/YouTubers:
**Content Performance Analysis:** Content creators can assess the performance of their videos, including likes, dislikes, views, comments, and audience engagement trends.
**Video Recommendations:** By identifying the top-performing videos, creators can refine their content strategy and produce more of what their audience enjoys.
**Audience Demographics:** Understand the demographics of their viewers to create content that appeals to their target audience.

#### Digital Marketing Agencies:
**Client Channel Management:** Digital marketing agencies managing multiple YouTube channels for clients can efficiently track and report on channel performance.
**Competitive Analysis:** Compare the performance of clients' channels with competitors to develop strategies for growth.
**ROI Tracking:** Assess the return on investment by analyzing which content generates the most views, likes, and comments.

#### Brands and Businesses:
**Product Promotion:** Analyze which videos have the most views and engagements, making informed decisions about which products or services to promote.
**Influencer Selection:** Identify and collaborate with influencers whose channels align with the brand's target audience and goals.
**Customer Feedback:** Monitor customer comments to gather feedback and address concerns.

#### Marketing and Sales Teams:
**Content Strategy:** Sales and marketing teams can use insights to align their content strategy with the preferences of their audience.
**Audience Engagement:** Understand the level of audience engagement and identify areas for improvement.
**Competitive Intelligence:** Track the performance of competitors' channels and develop strategies to outperform them.

#### Data Analysts and Researchers:
**Data Mining:** Researchers and data analysts can utilize the data collected to conduct research and gather insights into YouTube trends and user behavior.
**Academic Research:** Academic institutions can use the project to study the impact of social media on various aspects of society and culture.

#### Educators and Trainers:
**Content Relevance:** Educators can analyze which videos are most relevant to their curriculum and teaching methods.
**Audience Feedback:** Use audience comments to improve content delivery and address students' questions.

## Contributing
I welcome contributions! If you have suggestions, improvements, or new features to add, please fork the repository and submit a pull request.

## License
This project is under the MIT License.

## Author
Raghavendran S,  
Aspiring Data Scientist  
[LinkedIN Profile](https://www.linkedin.com/in/raghavendransundararajan/)  
raghavendranhp@gmail.com  

Thank You !  
Happy Enjoying !
