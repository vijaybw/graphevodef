## GraphEvoDef - Defect Prediction Using Deep learning with Network PortraitDivergence for Software Evolution

Understanding software evolution is essential for software development tasks, including debugging, maintenance, and testing. As a software system evolves, it grows in size and becomes more complex, hindering its comprehension. Researchers proposed several approaches for software quality analysis based on software metrics. One of the primary practices is predicting defects across software components in the code-base to improve agile product quality. While several software metrics exist, graph-based metrics have rarely been utilized in software quality. In this paper, we explore recent \textcolor{blue}{information} theory advancements to characterize software evolution and focus on aiding software visualization, metrics analysis, and defect prediction. We support our approach with an automated tool named GraphEvoDef. Particularly, GraphEvoDef aims at three-fold goals: It allows (1) to detect and visualize software evolution changes using call graphs, (2) analyze a set of metrics that can aid the software structure analysis, and (3) we recommend and utilize a set of metrics explicit for defect prediction using deep learning. In order to show the general usefulness of the approach of utilizing network divergence in software evolution, we examined 29 different open-source Java projects from GitHub and then demonstrated the proposed approach using 9 Java open-source projects with defect data from the PROMISE dataset. We then built and evaluated a defect prediction model. Our proposed technique has an 18\% reduction in the mean square error and a 48\% increase in squared correlation coefficient over the state-of-the-art approaches.

### Screenshots
#Creating new project through UI
  ## Uploading Jar files
  ![Screenshot2](https://user-images.githubusercontent.com/1021061/129414305-877c6070-4f59-4b62-ad35-4cb68bd1f3d2.png)
  ## Viewing complete call graph
  ![Screenshot0](https://user-images.githubusercontent.com/1021061/129414311-97556e41-622d-4b07-9b77-22e41c3ba775.png)
  ## Viewing Class metrics
  <img width="960" alt="Screenshot3" src="https://user-images.githubusercontent.com/1021061/129414323-e73c5772-ee23-4607-abdf-ffbe33541e0e.png">
 
### Details of Training Set
  ![image](https://user-images.githubusercontent.com/1021061/129462712-893dd5c7-60b6-4f08-909f-328056580b18.png)

