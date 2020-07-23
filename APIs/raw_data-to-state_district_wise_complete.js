const fs = require('fs');
const moment = require("moment");
const rawData = require('./raw_data');

console.log('Starting district wise data processing');
try {
  const StateDistrictWiseData = rawData.raw_data.reduce((acc, row) => {
    const isToday = moment().utcOffset(330).isSame(moment(row.dateannounced, "DD-MM-YYYY"), "day"); // used to increase data, nothing else
    let stateName = row.detectedstate; // get the state
    if(!stateName) {
      stateName = 'Unknown';
    }
    if(!acc[stateName]) {
      acc[stateName] = {districtData: {}}; // state -> districtData ->{all districts}
    }
    let districtName = row.detecteddistrict; // get district name
    if(!districtName) {
      districtName = 'Unknown';
    }
    if(!acc[stateName].districtData[districtName]) { // create an entry for district in districtData
      
      acc[stateName].districtData[districtName] = {
        confirmed: 0,
        active: 0,
        deaths: 0,
        recovered: 0,
        lastupdatedtime: "",
        delta: {
          confirmed: 0,
          active: 0,
          deaths: 0,
          recovered: 0
        }
      };
    }
    const currentDistrict = acc[stateName].districtData[districtName]; // get the district created in previous step
  
    currentDistrict.confirmed++;
    if (isToday) {
      currentDistrict.delta.confirmed++;
    }
    if(row.currentstatus === 'Hospitalized') {
      currentDistrict.active++;
      if(isToday) currentDistrict.delta.active++;
    } else if(row.currentstatus === 'Deceased') {
      currentDistrict.deaths++;
      if(isToday) currentDistrict.delta.deaths++;
    } else if(row.currentstatus === 'Recovered') {
      currentDistrict.recovered++;
      if(isToday) currentDistrict.delta.recovered++;
    }

    return acc;
  
  }, {});

  let stateDistrictWiseDataV2 = Object.keys(StateDistrictWiseData).map(state => {
    let districtData = StateDistrictWiseData[state].districtData;
    return {
      state,
      districtData: Object.keys(districtData).map(district => {
        return { district, ...districtData[district] };
      })
    }
  });

  fs.writeFileSync('state_district_wise_complete.json', JSON.stringify(StateDistrictWiseData, null, 2));
  fs.writeFileSync('./v2/state_district_wise_complete.json', JSON.stringify(stateDistrictWiseDataV2, null, 2));
  console.log('Starting district wise data processing ...done');
} catch(err) {
  console.log('Error processing district wise data', err);
}

