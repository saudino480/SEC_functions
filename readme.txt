What you see here is the hard work of Nelson Lam, Venkata Vemanedi, Joon-young Gawk, Sam Audino and Dr. Zhongjin Lu.

This project attempts to understand how a commodity company's hedging position influences their stock price. For instance, is an oil company that has a high hedging ratio (ie, amount hedged over amount produced) likely to see their stocks rise in the face of turbulence in the oil market? Are companies that take large amounts of risk (ie, low hedge ratios) more likely to see their stocks fall? 

While we were not able to completely understand the trends that occur due to a company's hedging ratio in the short two weeks that we had to finish the project, we were able to build an efficient ETL pipeline that ingested raw data scrapped directly from the SEC website and turn data that was formatted in many different ways into a uniform framework, as well as identifying what kind of commodity it was (oil, natural gas, liquid natural gas), as well as what instrument was used to hedge (swap, collar, put, etc). 

You will find in the /python_files directory the Jupyter Notebooks used to clean some of the individual tickers. The necessary pickle file has been included so that you can run the processes yourself and see how the data is transformed. You can find a simple overview of this process in the powerpoint "DSA Capstone Project.pdf". For a more indepth look, please feel free to either look into the individual helper files (sja_functions.py, zlu_functions.py, nel_functions.py) or contact me on GitHub or at saudino480@gmail.com.

Additionally, we have included the analysis, which is also summarised in "DSA Capstone Project.pdf".

Enjoy looking around,
Sam Audino
