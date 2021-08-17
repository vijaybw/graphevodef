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

### Metric Values

<table class="tableizer-table">
<thead><tr class="tableizer-firstrow"><th>Application</th><th>Version</th><th>Nodes</th><th>Edges</th><th>Paths</th><th>Avg-Degree</th><th>Clustering Coef</th><th>Diameter</th><th>Modularity</th></tr></thead><tbody>
 <tr><td>Antlr</td><td>antlr-4.0-complete</td><td>1897</td><td>3718</td><td>60290</td><td>1.96</td><td>0.038</td><td>16</td><td>0.853</td></tr>
 <tr><td>&nbsp;</td><td>antlr-4.1-complete</td><td>1914</td><td>3787</td><td>66850</td><td>1.979</td><td>0.038</td><td>16</td><td>0.837</td></tr>
 <tr><td>&nbsp;</td><td>antlr-4.2-complete</td><td>2075</td><td>3995</td><td>83121</td><td>1.925</td><td>0.037</td><td>16</td><td>0.848</td></tr>
 <tr><td>&nbsp;</td><td>antlr-4.4-complete</td><td>2334</td><td>4352</td><td>111242</td><td>1.865</td><td>0.037</td><td>16</td><td>0.846</td></tr>
 <tr><td>&nbsp;</td><td>antlr-4.5-complete</td><td>2596</td><td>4630</td><td>118115</td><td>1.784</td><td>0.035</td><td>16</td><td>0.86</td></tr>
 <tr><td>BroadleafCommerce</td><td>broadleaf-common-1.6.0-M2</td><td>236</td><td>213</td><td>292</td><td>0.903</td><td>0.015</td><td>5</td><td>0.943</td></tr>
 <tr><td>&nbsp;</td><td>broadleaf-common-2.0.0-ga</td><td>321</td><td>280</td><td>373</td><td>0.872</td><td>0.009</td><td>5</td><td>0.959</td></tr>
 <tr><td>&nbsp;</td><td>broadleaf-common-2.0.7-ga</td><td>317</td><td>279</td><td>372</td><td>0.88</td><td>0.013</td><td>5</td><td>0.958</td></tr>
 <tr><td>&nbsp;</td><td>broadleaf-common-2.4.0-GA</td><td>377</td><td>333</td><td>488</td><td>0.883</td><td>0.013</td><td>5</td><td>0.959</td></tr>
 <tr><td>&nbsp;</td><td>broadleaf-common-3.0.10-GA</td><td>521</td><td>453</td><td>661</td><td>0.869</td><td>0.013</td><td>5</td><td>0.967</td></tr>
 <tr><td>&nbsp;</td><td>broadleaf-common-3.1.0-M2-15</td><td>719</td><td>653</td><td>1028</td><td>0.908</td><td>0.012</td><td>5</td><td>0.962</td></tr>
 <tr><td>&nbsp;</td><td>broadleaf-common-4.0.0-BETA12</td><td>1075</td><td>1042</td><td>1841</td><td>0.969</td><td>0.011</td><td>5</td><td>0.956</td></tr>
 <tr><td>&nbsp;</td><td>broadleaf-common-4.0.0-GA</td><td>1128</td><td>1102</td><td>1967</td><td>0.977</td><td>0.012</td><td>5</td><td>0.95</td></tr>
 <tr><td>Camel</td><td>camel-1.0</td><td>1163</td><td>1059</td><td>2348</td><td>0.911</td><td>0.01</td><td>9</td><td>0.975</td></tr>
 <tr><td>&nbsp;</td><td>camel-2.0</td><td>2038</td><td>1991</td><td>4885</td><td>0.977</td><td>0.013</td><td>10</td><td>0.97</td></tr>
 <tr><td>Hazelcast</td><td>hazelcast-2.1</td><td>2348</td><td>3351</td><td>9369</td><td>1.427</td><td>0.013</td><td>9</td><td>0.816</td></tr>
 <tr><td>&nbsp;</td><td>hazelcast-2.4</td><td>2458</td><td>3525</td><td>10560</td><td>1.434</td><td>0.014</td><td>11</td><td>0.811</td></tr>
 <tr><td>&nbsp;</td><td>hazelcast-2.5.1</td><td>2488</td><td>3576</td><td>10962</td><td>4.437</td><td>0.013</td><td>11</td><td>0.803</td></tr>
 <tr><td>&nbsp;</td><td>hazelcast-3.1.1</td><td>4605</td><td>6223</td><td>11274</td><td>1.351</td><td>0.009</td><td>7</td><td>0.86</td></tr>
 <tr><td>&nbsp;</td><td>hazelcast-3.3-EA</td><td>5929</td><td>7874</td><td>14933</td><td>1.328</td><td>0.008</td><td>6</td><td>0.887</td></tr>
 <tr><td>&nbsp;</td><td>hazelcast-3.4-EA</td><td>6912</td><td>8895</td><td>15561</td><td>1.287</td><td>0.007</td><td>6</td><td>0.919</td></tr>
 <tr><td>&nbsp;</td><td>hazelcast-3.5-EA</td><td>8779</td><td>12352</td><td>22720</td><td>1.407</td><td>0.007</td><td>10</td><td>0.911</td></tr>
 <tr><td>Ivy</td><td>ivy-2.0</td><td>1214</td><td>1833</td><td>11356</td><td>1.51</td><td>0.014</td><td>8</td><td>0.766</td></tr>
 <tr><td>&nbsp;</td><td>ivy-1.4</td><td>2064</td><td>3107</td><td>6896</td><td>1.505</td><td>0.015</td><td>8</td><td>0.774</td></tr>
 <tr><td>Lucene</td><td>lucene-2.0</td><td>852</td><td>1272</td><td>2613</td><td>1.493</td><td>0.022</td><td>7</td><td>0.84</td></tr>
 <tr><td>&nbsp;</td><td>lucene-2.2</td><td>1059</td><td>1568</td><td>5098</td><td>1.481</td><td>0.02</td><td>8</td><td>0.826</td></tr>
 <tr><td>&nbsp;</td><td>lucene-2.4</td><td>1677</td><td>2580</td><td>6364</td><td>1.538</td><td>0.018</td><td>9</td><td>0.811</td></tr>
 <tr><td>Mapdb</td><td>mapdb-0.9.0</td><td>314</td><td>474</td><td>1120</td><td>1.51</td><td>0.03</td><td>6</td><td>0.783</td></tr>
 <tr><td>&nbsp;</td><td>mapdb-0.9.13</td><td>476</td><td>849</td><td>2912</td><td>1.784</td><td>0.036</td><td>7</td><td>0.784</td></tr>
 <tr><td>&nbsp;</td><td>mapdb-0.9.6</td><td>438</td><td>749</td><td>2279</td><td>1.71</td><td>0.038</td><td>7</td><td>0.798</td></tr>
 <tr><td>&nbsp;</td><td>mapdb-1.0.5</td><td>471</td><td>842</td><td>2893</td><td>1.788</td><td>0.036</td><td>7</td><td>0.784</td></tr>
 <tr><td>&nbsp;</td><td>mapdb-1.0.7</td><td>471</td><td>843</td><td>2895</td><td>1.79</td><td>0.034</td><td>7</td><td>0.785</td></tr>
 <tr><td>&nbsp;</td><td>mapdb-2.0-alpha3</td><td>421</td><td>831</td><td>3619</td><td>1.974</td><td>0.042</td><td>7</td><td>0.752</td></tr>
 <tr><td>mcMMO</td><td>mcMMO-1.3.09</td><td>12</td><td>10</td><td>12</td><td>0.833</td><td>0</td><td>2</td><td>0.535</td></tr>
 <tr><td>&nbsp;</td><td>mcMMO-1.3.14</td><td>18</td><td>16</td><td>19</td><td>0.889</td><td>0</td><td>2</td><td>0.602</td></tr>
 <tr><td>&nbsp;</td><td>mcMMO-1.4.08</td><td>14</td><td>15</td><td>17</td><td>1.071</td><td>0.046</td><td>1</td><td>0.398</td></tr>
 <tr><td>&nbsp;</td><td>mcMMO-1.5.00</td><td>14</td><td>15</td><td>17</td><td>1.071</td><td>0.046</td><td>1</td><td>0.398</td></tr>
 <tr><td>Netty</td><td>netty-3.2.4.Final</td><td>988</td><td>890</td><td>1200</td><td>0.901</td><td>0.009</td><td>5</td><td>0.967</td></tr>
 <tr><td>&nbsp;</td><td>netty-3.2.5.Final</td><td>988</td><td>891</td><td>1202</td><td>0.902</td><td>0.009</td><td>5</td><td>0.966</td></tr>
 <tr><td>&nbsp;</td><td>netty-3.3.1.Final</td><td>1141</td><td>999</td><td>1324</td><td>0.876</td><td>0.007</td><td>5</td><td>0.973</td></tr>
 <tr><td>&nbsp;</td><td>netty-3.5.4.Final</td><td>1428</td><td>1222</td><td>1741</td><td>0.856</td><td>0.006</td><td>5</td><td>0.974</td></tr>
 <tr><td>&nbsp;</td><td>netty-3.9.3.Final</td><td>1631</td><td>1507</td><td>2308</td><td>0.924</td><td>0.008</td><td>5</td><td>0.924</td></tr>
 <tr><td>&nbsp;</td><td>netty-all-4.0.0.Beta2</td><td>2172</td><td>2177</td><td>3375</td><td>1.002</td><td>0.016</td><td>6</td><td>0.966</td></tr>
 <tr><td>&nbsp;</td><td>netty-all-4.0.16.Final</td><td>2902</td><td>3795</td><td>5473</td><td>1.308</td><td>0.011</td><td>5</td><td>0.827</td></tr>
 <tr><td>&nbsp;</td><td>netty-all-4.0.7.Final</td><td>2745</td><td>3553</td><td>5000</td><td>1.294</td><td>0.011</td><td>5</td><td>0.836</td></tr>
 <tr><td>Poi</td><td>poi-2.0</td><td>2349</td><td>3054</td><td>7463</td><td>1.3</td><td>0.014</td><td>7</td><td>0.881</td></tr>
 <tr><td>&nbsp;</td><td>poi-2.5</td><td>2907</td><td>3784</td><td>8763</td><td>1.302</td><td>0.014</td><td>7</td><td>0.896</td></tr>
 <tr><td>&nbsp;</td><td>poi-3.0</td><td>3566</td><td>4896</td><td>13049</td><td>1.373</td><td>0.014</td><td>7</td><td>0.894</td></tr>
 <tr><td>Titan</td><td>titan-0.1.0</td><td>598</td><td>580</td><td>855</td><td>0.97</td><td>0.011</td><td>5</td><td>0.94</td></tr>
 <tr><td>&nbsp;</td><td>titan-core-0.2.1</td><td>542</td><td>5000</td><td>758</td><td>0.923</td><td>0.007</td><td>5</td><td>0.949</td></tr>
 <tr><td>&nbsp;</td><td>titan-core-0.4.0</td><td>726</td><td>806</td><td>2491</td><td>1.11</td><td>0.011</td><td>6</td><td>0.884</td></tr>
 <tr><td>&nbsp;</td><td>titan-core-0.4.4</td><td>873</td><td>950</td><td>2713</td><td>1.088</td><td>0.012</td><td>7</td><td>0.89</td></tr>
 <tr><td>&nbsp;</td><td>titan-core-0.5.1</td><td>1568</td><td>1797</td><td>10794</td><td>1.146</td><td>0.015</td><td>12</td><td>0.872</td></tr>
 <tr><td>&nbsp;</td><td>titan-core-0.5.4</td><td>1606</td><td>1833</td><td>10840</td><td>1.141</td><td>0.014</td><td>12</td><td>0.869</td></tr>
 <tr><td>Velocity</td><td>velocity-1.4</td><td>463</td><td>663</td><td>32690</td><td>1.432</td><td>0.024</td><td>15</td><td>0.813</td></tr>
 <tr><td>&nbsp;</td><td>velocity-1.5</td><td>732</td><td>968</td><td>38970</td><td>1.322</td><td>0.018</td><td>15</td><td>0.817</td></tr>
 <tr><td>&nbsp;</td><td>velocity-1.6</td><td>751</td><td>1002</td><td>43204</td><td>1.334</td><td>0.019</td><td>16</td><td>0.823</td></tr>
 <tr><td>Xalan</td><td>xalan-2.4</td><td>1069</td><td>1885</td><td>10437</td><td>1.763</td><td>0.029</td><td>11</td><td>0.78</td></tr>
 <tr><td>&nbsp;</td><td>xalan-2.5</td><td>2193</td><td>3986</td><td>13681</td><td>1.818</td><td>0.023</td><td>11</td><td>0.79</td></tr>
 <tr><td>&nbsp;</td><td>xalan-2.6</td><td>2391</td><td>4243</td><td>14218</td><td>1.775</td><td>0.022</td><td>11</td><td>0.8</td></tr>
 <tr><td>&nbsp;</td><td>xalan-2.7</td><td>2445</td><td>4378</td><td>14792</td><td>1.791</td><td>0.022</td><td>11</td><td>0.805</td></tr>
 <tr><td>Xerces</td><td>xerces-1.2</td><td>1254</td><td>2385</td><td>15438</td><td>1.902</td><td>0.056</td><td>10</td><td>0.79</td></tr>
 <tr><td>&nbsp;</td><td>xerces-1.3</td><td>1346</td><td>2566</td><td>21211</td><td>1.906</td><td>0.055</td><td>10</td><td>0.787</td></tr>
</tbody></table>
