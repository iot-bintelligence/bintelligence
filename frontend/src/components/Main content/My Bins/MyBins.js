import './MyBins.css'
import Bin from '../My Bins/Bin'
import React, { useState, useEffect } from 'react';



function MyBins() {
  const [data, setData] = useState(null);

  useEffect(() => {
    async function fetchData() {
      const response = await fetch('https://eit.hjelmtvedt.io/api/prediction');
      const json = await response.json();
      setData(json);
    }
    fetchData();
  }, []);

  if (!data) {
    return <div>Loading...</div>;
  }




  return (
    <div className="binContainer">
      <h1>Mine komprimatorer</h1>
      <div className="mybins">
        <Bin name={"Roverud sykehjem"} fillDegree={data.percent} estimate={data.time}/>
        <Bin name={"Langeland sykehjem"} fillDegree={data.percent} estimate={data.time}/>
      </div>
        
    </div>
  )
}

export default MyBins;