Skip to main contentSkip to article
Elsevier logo
Journals & Books

Help
Search
My account
Sign in
Purchase PDF
Article preview
Abstract
Introduction
Section snippets
References (53)
Cited by (6)
Elsevier
Journal of Systems and Software
Volume 159, January 2020, 110451
Journal of Systems and Software
In Practice
Using Orthogonal Defect Classification to characterize NoSQL database defects
Author links open overlay panel
João Agnelo
, 
Nuno Laranjeiro
, 
Jorge Bernardino 1

Show more

Add to Mendeley

Share

Cite
https://doi.org/10.1016/j.jss.2019.110451
Get rights and content
Highlights
•
Orthogonal Defect Classification applied to a large set of software defects of NoSQL databases.
•
MongoDB, Cassandra, and HBase tend to be affected by the same kinds of software defects.
•
The types of defects found in NoSQL databases follow a unique distribution not previously seen in related work.
•
We provide an open dataset holding 4096 bug reports classified using ODC.
Abstract
NoSQL databases are increasingly used for storing and managing data in business-critical Big Data systems. The presence of software defects (i.e., bugs) in these databases can bring in severe consequences to the NoSQL services being offered, such as data loss or service unavailability. Thus, it is essential to understand the types of defects that frequently affect these databases, allowing developers take action in an informed manner (e.g., redirect testing efforts). In this paper, we use Orthogonal Defect Classification (ODC) to classify a total of 4096 software defects from three of the most popular NoSQL databases: MongoDB, Cassandra, and HBase. The results show great similarity for the defects across the three different NoSQL systems and, at the same time, show the differences and heterogeneity regarding research carried out in other domains and types of applications, emphasizing the need for possessing such information. Our results expose the defect distributions in NoSQL databases, provide a foundation for selecting representative defects for NoSQL systems, and, overall, can be useful for developers for verifying and building more reliable NoSQL database systems.
Introduction
In recent years, we observed a noticeable growth in the use of NoSQL Database Management Systems that nowadays compete with the older and much more mature, Relational Databases. This evolution derives from the needs of the Big Data era, namely the need for supporting high data volumes, high velocity, and also variety (i.e., different forms of data), along with easier horizontal scalability (Leavitt, 2010). In these systems, losing data or being unable to use the storage service has negative consequences not only for the user, but also for the provider, that sees its reputation affected. Such events are many times the result of the presence of a defect in the software (Marks, 2014; Hulme, 2017).
Software defects (i.e., bugs) can range from simple spelling or grammar mistakes in user messages, to security vulnerabilities which, once exploited, may result in disclosure of private information or in infrastructure damage (Avizienis et al., 2004), for example. There are many cases of software defects that have led to disastrous consequences, from misguided space rockets, to crashing military airplanes, and ultimately, human deaths (Mellor, 1994). For the sake of dependability, any software defect found should be fixed in due time. Otherwise, and this is especially true for high priority defects (e.g., defects that for instance impair the core capabilities of the system) the product reputation may collapse to an irrecoverable level (this may also apply to the company behind the product, or the one using it). In the case of the most popular NoSQL databases, the identification and fixing of bugs is largely supported by their large communities, which actively find software defects, report them in an issue-tracking platform, and trigger their correction.
Understanding the nature of software defects (e.g., by using structured methods for defect classification Chillarege, 1996; IEEE Standard Classification for Software Anomalies 2010; Grady, 1992) can provide extremely useful information for developers, who can better focus their software verification efforts or, for instance, concentrate their development efforts in certain components or code areas known to be prone to a particular software defect type (Chillarege, 1996). This kind of effort has been undertaken for many and very different types of software that operate in distinct domains, including browsers, games, operating systems, satellite software, business-critical applications, build systems, or machine learning software, just to name a few (Durães and Madeira, 2006; Thung et al., 2012; Xia et al., 2013; Silva et al., 2017). Many times, the general hypothesis placed is that the specificities involving the system (e.g., programming language, project nature and requirements, type and experience of the application development team) make it necessary for such specific analysis to take place. In this context, the analysis of defects affecting storage intensive systems (i.e., NoSQL databases, in the case of this work) has been disregarded so far.
In this paper, we analyze the defects of three of the most popular NoSQL databases: MongoDB (2019), Cassandra (Apache Software Foundation, 2019), and HBase (Apache Software Foundation 2019b). We begin by training one researcher with the application of Orthogonal Defect Classification (ODC) (Chillarege, 1996) against a total of 300 defects affecting these databases. We discard the training dataset (to avoid using a potentially low-quality annotated dataset, as the quality of the ODC labelling tends to increase with the experience of the annotator) and then analyze a set of 4096 defects extracted from the databases’ issue-tracking systems and manually classify them with ODC using the previously trained ODC researcher and according to six of the eight ODC attributes (the age and source ODC attributes were not considered due to the general lack of information in the defect reports regarding these two cases). We internally double-check the classification result for 20% (i.e., 820 bugs) of the defects and then ask for two external and ODC-knowledgeable researchers to produce independent ODC classifications for an additional 20% of the total defects (10% per researcher). The outcome of the verification carried out by the external researchers revealed the overall good quality of the dataset, with almost perfect Cohen's Kappa agreements (Cohen, 1960) found for the majority of the ODC attributes involved.
We then analyze the resulting dataset of ODC-classified defects according to the following four perspectives: (i) we analyze the distribution of values concerning six of the eight existing ODC attributes (e.g., type of defect, conditions that trigger the defect, impact of the defect); (ii) we form pairs of attributes and analyze the value distributions, as in related work (e.g., Chillarege, 1996; Durães and Madeira, 2006; Zhi-bo et al., 2011); (iii) we analyze the defect type distribution in the top 3 most affected components per each database; and (iv) we analyze our results in perspective with previous work. We also describe a practical use case to show how this kind of analysis may be beneficial for developers by generating tests to target a database component showing high prevalence of checking defects.
We observed a huge variation in the distribution of defect types found in related work, which goes through the defects of various types of applications from other domains, such as browsers, operating systems, satellite onboard software, machine learning tools, or build tools. Our results have confirmed this heterogeneity, which in practice means that we cannot assume, a priori, the existence of a certain defect distribution. This implies that this kind of study must be carried out whenever it is important to know which are the representative defects for a certain type of system, built in specific conditions. In this work, we actually observed a unique distribution of values (i.e., in terms of the relative popularity of the types of defects found), that is not present in any of the related work analyzed. The results suggest that the overall nature of the system may be a factor that influences the distribution of defects.
We also observed great similarity across the three databases, when inspecting the results for the individual ODC attributes. Sometimes, a single value dominated the distribution. When crossing pairs of attributes, three of the main observations include: (i) the fact that testing activities are more than two times more frequently associated with reliability defects than with capability defects; (ii) checking defects (e.g., input validation) are more frequent when the impact is reliability; and (iii) checking defects are more likely to be associated with the “missing” qualifier. We also noticed disparities in the distribution of defect types in different system components, which may be justified with the nature of the component (e.g., a replication component holding Timing/Serialization defects), and, finally, we found certain types of defects being consistently associated with longer times to fix across all three databases (e.g., Function/Class/Object).
Overall, our results (available in detail, along with supporting code, at Agnelo et al., 2019) confirm the need for understanding the defect trends in NoSQL systems and bring insight regarding their defect distribution. The main contributions of this paper are the following:
•
We use Orthogonal Defect Classification to provide a detailed view over a relatively large dataset of reported bugs in three popular NoSQL databases, including a view on the most affected database components;
•
We show our results in perspective with the very heterogeneous related work, signaling differences and also similarities found;
•
We provide an open dataset holding 4096 bug reports classified using ODC and freely available for future research (Agnelo et al., 2019).
The kind of analysis carried out in this paper can serve for process improvement in a variety of ways (e.g., performing root cause analysis Silva et al., 2017), as the analysis of field data using ODC, in general allows for better defect prevention and detection (IBM 2013) (e.g., a known tendency for having a certain type of defect in a certain component of the system represents essential information for practitioners). Thus, the data allow practitioners to obtain knowledge regarding the overall reliability – or lack thereof – of their systems, but it could also help to improve the quality of the development processes, for instance by directing verification efforts to the appropriate areas (e.g., design, algorithm) or selecting certain verification techniques (e.g., testing, code inspections). Researchers may benefit from this type of results and use them as basis for creating new verification techniques for this kind of systems (e.g., fault injection based techniques using the defect information obtained from this work, as in Durães and Madeira, 2006); or even for tailoring development processes (Børretzen and Dyre-Hansen, 2007) to specifically consider the specificities of this kind of systems and the nature of the defects that typically affects NoSQL databases.
The remainder of this paper is organized as follows. Section II presents background on ODC and discusses the related work. Section III describes our approach for classifying the extracted defects and Section IV presents and analyses the results. Section V discusses the main findings of this work and Section VI presents the threats to the validity of the work. Finally, Section VII concludes the paper.
Section snippets
Background and related work
In this section, we briefly go through the main software defect classification schemes used nowadays, with focus on the main concepts regarding the Orthogonal Defect Classification, and we then discuss the related work.
Study design
This section describes the design of our study, which has the general goal of understanding the overall nature of software defects present in NoSQL databases. With the resulting defect classification, we will be mostly aiming at:
(i)
Understanding if the types of defects (across the different ODC attributes) that tend affect this class of systems are consistently the same (or not) across different NoSQL databases. In practice, this is evidence of some shared nature between the three systems.
(ii)
Results
In this section, we describe the results obtained from applying ODC to the 4096 defects collected from the issue-tracking platforms of the three previously mentioned NoSQL databases. We first analyze the distribution of values obtained for each individual ODC attribute, we then analyze the results for pairs of ODC attributes and conclude with a detailed view on the most affected components per database. All detailed results and also supporting code are available at (Agnelo et al., 2019).
Discussion
In this section, we highlight and further discuss the main results presented in the previous section and put them in perspective with the results analyzed in related work.
The results obtained in this work, in particular for the single attribute analysis presented earlier, show that, regardless of the attribute being considered, defects extracted from different systems tend to concentrate around just a few attribute values (e.g., among the thirteen existing impact values, “Capability” and
Threats to validity
In this section, we present threats to the validity of this work and discuss mitigation strategies. We start by mentioning the fact that, in this work, we have analyzed 4096 bug reports, which is a subset of all reported bugs affecting the studied NoSQL databases (about one fourth of the total number of bug reports). Thus, our results may not be representative of the whole population of bugs affecting these systems. This option for a subset of bugs was due to the huge amount of human effort
Conclusion
In this paper, we analyzed software defects reported for three of the most popular NoSQL databases using Orthogonal Defect Classification. The application of the ODC procedure was entirely manual, and we internally double checked the results and also asked two independent early stage researchers to perform an external verification. The outcome of both verification procedures indicate the overall good quality of the dataset, which we make publicly available at Agnelo et al. (2019).
We have
Acknowledgments
This work has been partially supported by the European Union’s Horizon 2020 research and innovation program under the Marie Sklodowska-Curie grant agreement No 823788 (project ADVANCE); by the project METRICS, funded by the Portuguese Foundation for Science and Technology (FCT)–agreement no POCI-01-0145-FEDER-032504; and by the project MobiWise: From mobile sensing to mobility advising (P2020 SAICTPAC/0011/2015), co-financed by COMPETE 2020, Portugal 2020 - Operational Program for
João Agnelo is an MSc student in Informatic Engineering at the Faculty of Sciences and Technology of the University of Coimbra. He concluded his BSc in Informatics Engineering at ISEC - Polytechnic Institute of Coimbra, in 2018. Alongside his studies, he is also currently working in a few research projects at CISUC - Centre for Informatics and Systems of the University of Coimbra. His-interests include dependability, artificial intelligence and computer graphics.
References (53)
N. Silva et al.
A field study on root cause analysis of defects in space software
Reliab. Eng. Syst. Saf.
(2017)
L. Zhi-bo et al.
Analysis of software process effectiveness based on orthogonal defect classification
Proced. Environ. Sci.
(2011)
Agnelo, J., Laranjeiro, N., Bernardino, J. “NoSQL odc dataset, results, and support code,” Mar-2019. [Online]....
Apache Software Foundation, “Apache Cassandra,” Apache Cassandra. [Online]. Available: http://cassandra.apache.org/,...
Apache Software Foundation, “Apache HBase,” Apache HBase. [Online]. Available:https://hbase.apache.org/,...
Apache Cassandra Unit Testing Code
(2019)
A. Avizienis et al.
Basic concepts and taxonomy of dependable and secure computing
IEEE Trans. Dependable Secure Comput.
(2004)
T. Basso et al.
An investigation of java faults operators derived from a field data study on java software faults
J.A. Børretzen et al.
Investigating the software fault profile of industrial projects to determine process improvement areas: an empirical study
R. Cattell
Scalable sql and nosql data stores
SIGMOD Rec
(2011)

View more references
Cited by (6)
Concerns identified in code review: A fine-grained, faceted classification
2023, Information and Software Technology
Citation Excerpt :
Since CRAM is the most detailed classification existing, we compared our classification to CRAM in detail in Section 5.4. There are many other manual defect classifications available [43–58]. They extract defects from various resources such as test reports and customer feedback reports [53].


Show abstract
Measuring in-service traction elevator reliability based on orthogonal defect classification and Markov analysis
2024, Proceedings of the Institution of Mechanical Engineers, Part O: Journal of Risk and Reliability
Injecting software faults in Python applications: The OpenStack case study
2022, Empirical Software Engineering
Application of Orthogonal Defect Classification for Software Reliability Analysis
2022, Probabilistic Safety Assessment and Management, PSAM 2022
Comparison of Graph- and Collection-Based Representations of Early Modern Biographical Archives
2022, CEUR Workshop Proceedings
Impact of Data Compression on the Performance of Column-oriented Data Stores
2021, International Journal of Advanced Computer Science and Applications
João Agnelo is an MSc student in Informatic Engineering at the Faculty of Sciences and Technology of the University of Coimbra. He concluded his BSc in Informatics Engineering at ISEC - Polytechnic Institute of Coimbra, in 2018. Alongside his studies, he is also currently working in a few research projects at CISUC - Centre for Informatics and Systems of the University of Coimbra. His-interests include dependability, artificial intelligence and computer graphics.
Nuno Laranjeiro received the Ph.D degree in 2012 from the University of Coimbra, Portugal, where he currently is an assistant professor. His research focuses on robust software services as well as experimental dependability evaluation, web services interoperability, services security, and enterprise application integration. He has authored more than 50 papers in refereed conferences and journals in the dependability and services computing areas.
Jorge Bernardino is a Coordinator Professor at the Polytechnic of Coimbra - ISEC, Portugal. He received the PhD degree from the University of Coimbra in 2002. His main research interests are Big Data, NoSQL, Data Warehousing, Software Engineering, and experimental databases evaluation. He has authored over 200 publications in refereed journals, book chapters, and conferences. He was President of ISEC from 2005 to 2010 and President of ISEC Scientific Council from 2017 to 2019. During 2014 he was Visiting Professor at CMU - Carnegie Mellon University, USA. He participated in several national and international projects and is an ACM and IEEE member. Currently, he is Director of Applied Research Institute of the Polytechnic of Coimbra, Portugal.
1
ISEC – Polytechnic of Coimbra, Portugal.
View full text
© 2019 Elsevier Inc. All rights reserved.

Part of special issue
Special Section on In Practice; Edited by Prof. Daniel Mendez Fernandez and Prof. Wesley Klewerton Guez Assunção
Edited by Daniel Mendez Fernandez Blekinge Institute of Technology, Wesley Klewerton Guez Assunção North Carolina State University
View special issue

Recommended articles
A data replication strategy with tenant performance and provider economic profit guarantees in Cloud data centers
Journal of Systems and Software, Volume 159, 2020, Article 110447
Riad Mokadem, Abdelkader Hameurlain
In-the-field monitoring of functional calls: Is it feasible?
Journal of Systems and Software, Volume 163, 2020, Article 110523
Oscar Cornejo, …, Leonardo Mariani
Feature dependencies in automotive software systems: Extent, awareness, and refactoring
Journal of Systems and Software, Volume 160, 2020, Article 110458
Andreas Vogelsang

Show 3 more articles

Article Metrics
Citations
Citation Indexes
6
Captures
Mendeley Readers
42
PlumX Metrics Logo
View details
Elsevier logo with wordmark
About ScienceDirect
Remote access
Advertise
Contact and support
Terms and conditions
Privacy policy
Cookies are used by this site. 
Cookie Settings

All content on this site: Copyright © 2025 Elsevier B.V., its licensors, and contributors. All rights are reserved, including those for text and data mining, AI training, and similar technologies. For all open access content, the relevant licensing terms apply.

RELX group home page