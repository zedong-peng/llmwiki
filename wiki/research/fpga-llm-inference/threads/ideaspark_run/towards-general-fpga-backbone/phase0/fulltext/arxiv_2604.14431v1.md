# AndroScanner: Automated Backend Vulnerability Detection for Android Applications

paper_id: arxiv:2604.14431v1
tier: T3
source_used: html_arxiv
warning: none

## Intro

More than 5.3 billion people use mobile applications
[
1
]
. Around 90 percent of individuals rely on smartphones. Roughly about 40 apps exist on each of these phones. Mobile backends provide various features such as content delivery, ad networks, telemetry, and more. These features are supported by several layers of software and multiple vendors including cloud providers, hosting providers, and content delivery networks (CDNs) that offer managed platforms, operating systems, and physical/virtual hardware. The inherent complexity of these backends makes secure deployment and maintenance difficult. As a result, when selecting these infrastructures for creating or renting mobile backends, application developers frequently overlook the security standards.
[
2
]
Backend breaches of mobile applications which happened recently indicate how prevalent these attacks are. The Fortnite mobile game hijacking
[
3
]
demonstrated how progressively downloaded material from mobile backends can allow an attacker to install new mobile apps without the user’s knowledge.
Even if the developer is security conscious, because of third-party libraries, it is unclear with which backends their mobile app will interface. Third-party libraries do not reveal their backends to developers; instead, they provide an application program interface (API) via which developers may interact. Many of these risks are avoidable if developers have the necessary tools and resources to assess the security of their backends. Furthermore, identifying insecure software layers and the responsible party helps speed up the remediation, lowering the risk of exposure.
Unfortunately, existing solutions like Drozer
[
4
]
demand practical recommendations for mobile app developers. The latest study on server-side vulnerability detection of mobile apps
[
7
,
8
,
9
]
also has revealed that app developers’ lack of security knowledge is a rising issue. However, by focusing solely on the software service layer of mobile backends, these studies merely scrape the surface.
To identify the most significant difficulties impacting mobile backends, a thorough analysis of APIs is required. Furthermore, in order to carry out such a study, the analysis must be reproducible, transparent, and simple for developers to comprehend. The research should be conducted on a representative mobile app ecosystem in order to offer a clear picture of the backend vulnerability environment. Finally, the research should provide vulnerabilities to follow in order to assist and inform them about the security of their mobile backends.
To the end, this paper presents the design and implementation of
AndroScanner
, an automated analysis pipeline to study mobile backends. Using
AndroScanner
, I have tested two applications, Bank App which is a vulnerable application
[
5
]
, and the
Hirect
application
[
6
]
which has over 50k+ downloads on Google Playstore.
AndroScanner
retrieves a list of backend APIs from an input APK, using remote vetting techniques to discover software vulnerabilities and accountable parties, and offers a list of existing vulnerabilities to the app developer. Findings discuss the total number of vulnerabilities present in each of these applications considering different scenarios.

## Method

The design for
AndroScanner
can be broken down into three major parts. They are as follows:
1.
Extracting API calls using Static Analysis and Dynamic Analysis.
2.
Vetting the extracted APIs for vulnerabilities.
3.
Reporting the list of vulnerabilities to the target user.
Figure
1
depicts the whole design of the system. Let’s deep dive into each of the implementation steps.
Figure 1:
Workflow of AndroScanner
