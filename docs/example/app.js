// Application data
const data = {
  "spending_comparison": [
    {"region": "United States", "spending": 14570, "continent": "North America"},
    {"region": "OECD Average", "spending": 7393, "continent": "Developed"},
    {"region": "European Average", "spending": 6000, "continent": "Europe"},
    {"region": "Sub-Saharan Africa Avg", "spending": 85, "continent": "Africa"},
    {"region": "Madagascar", "spending": 18, "continent": "Africa"},
    {"region": "Chad", "spending": 36, "continent": "Africa"},
    {"region": "Niger", "spending": 34, "continent": "Africa"},
    {"region": "Ethiopia", "spending": 26, "continent": "Africa"}
  ],
  "workers_comparison": [
    {"region": "Americas", "workers": 24.8, "continent": "Americas"},
    {"region": "Europe Average", "workers": 13.0, "continent": "Europe"},
    {"region": "WHO Threshold", "workers": 4.45, "continent": "Standard"},
    {"region": "Global Average", "workers": 9.5, "continent": "Global"},
    {"region": "Africa", "workers": 1.55, "continent": "Africa"},
    {"region": "Niger (Lowest)", "workers": 0.25, "continent": "Africa"}
  ],
  "hospital_beds": [
    {"region": "Japan", "beds": 12.6, "continent": "Asia"},
    {"region": "South Korea", "beds": 12.8, "continent": "Asia"},
    {"region": "Germany", "beds": 7.8, "continent": "Europe"},
    {"region": "OECD Average", "beds": 4.3, "continent": "Developed"},
    {"region": "Global Average", "beds": 2.7, "continent": "Global"},
    {"region": "Africa Average", "beds": 1.0, "continent": "Africa"},
    {"region": "Mali (Lowest)", "beds": 0.1, "continent": "Africa"}
  ],
  "burden_vs_workers": [
    {"category": "Disease Burden", "africa_share": 25, "worker_share": 3},
    {"category": "Population", "africa_share": 17, "worker_share": 3}
  ],
  "shortage_projection": [
    {"year": 2022, "shortage": 5.6, "projected": false},
    {"year": 2030, "shortage": 6.1, "projected": true}
  ],
  "african_spending_detail": [
    {"country": "Seychelles", "spending": 718, "category": "High"},
    {"country": "South Africa", "spending": 584, "category": "High"},
    {"country": "Mauritius", "spending": 565, "category": "High"},
    {"country": "Botswana", "spending": 457, "category": "Medium"},
    {"country": "Ghana", "spending": 100, "category": "Low"},
    {"country": "Kenya", "spending": 95, "category": "Low"},
    {"country": "Nigeria", "spending": 84, "category": "Low"},
    {"country": "Uganda", "spending": 43, "category": "Very Low"},
    {"country": "Ethiopia", "spending": 26, "category": "Very Low"},
    {"country": "Madagascar", "spending": 18, "category": "Very Low"}
  ]
};

// AI Infrastructure data
const aiData = {
  "physical_infrastructure": [
    {"metric": "Internet Penetration", "africa": 38, "global": 68, "developed": 85, "unit": "% population"},
    {"metric": "Data Center Capacity", "africa": 0.8, "americas": 88.5, "europe": 73.9, "asia": 28.7, "unit": "MW per million people"},
    {"metric": "Reliable Electricity", "africa": 43, "global": 78, "developed": 95, "unit": "% population"},
    {"metric": "5G Coverage", "africa": 11, "global": 35, "developed": 70, "unit": "% population"},
    {"metric": "Broadband Household Penetration", "africa": 12, "global": 62, "developed": 80, "unit": "% households"}
  ],
  "human_capital": [
    {"metric": "Digital Skills Index", "africa_avg": 3.4, "global_avg": 6.0, "developed_avg": 8.2},
    {"metric": "Computer Skills in Curriculum", "africa": 50, "global": 85, "unit": "% of countries"},
    {"metric": "Children Leaving School with Digital Skills", "africa": 10, "global": 60, "developed": 85, "unit": "% of children"},
    {"metric": "AI/ML University Programs", "africa": 62, "global": 2400, "unit": "% concentrated in 3 countries only"},
    {"metric": "Digital Job Readiness", "africa": 23, "global": 45, "developed": 72, "unit": "% of workforce"}
  ],
  "regulatory_framework": [
    {"metric": "Comprehensive AI Strategies", "africa": 8, "developed": 35, "unit": "countries"},
    {"metric": "Advanced ICT Regulation (G4)", "africa": 18, "global": 38, "unit": "% of countries"},
    {"metric": "Data Protection Laws", "africa": 35, "global": 75, "developed": 95, "unit": "% of countries"},
    {"metric": "AI Ethics Frameworks", "africa": 15, "global": 45, "developed": 80, "unit": "% of countries"}
  ],
  "economic_ecosystem": [
    {"metric": "VC Funding per Capita", "africa": 1.8, "global": 45, "us": 180, "unit": "USD per capita"},
    {"metric": "Tech Unicorns", "africa": 7, "us": 600, "china": 350, "europe": 120, "unit": "companies"},
    {"metric": "R&D Spending", "africa": 0.3, "global": 2.4, "developed": 3.2, "unit": "% of GDP"},
    {"metric": "Tech Startup Density", "africa": 2.3, "global": 8.7, "developed": 15.4, "unit": "per 1000 businesses"}
  ],
  "ai_readiness_scores": [
    {"country": "United States", "score": 88, "region": "North America"},
    {"country": "Singapore", "score": 85, "region": "Asia"},
    {"country": "Germany", "score": 82, "region": "Europe"},
    {"country": "South Korea", "score": 80, "region": "Asia"},
    {"country": "Global Average", "score": 55, "region": "Global"},
    {"country": "South Africa", "score": 42, "region": "Africa"},
    {"country": "Kenya", "score": 35, "region": "Africa"},
    {"country": "Nigeria", "score": 32, "region": "Africa"},
    {"country": "Ghana", "score": 28, "region": "Africa"},
    {"country": "Africa Average", "score": 25, "region": "Africa"}
  ],
  "healthcare_ai_potential": [
    {"application": "Remote Diagnostics", "potential_impact": 85, "infrastructure_readiness": 25, "gap": 60},
    {"application": "Drug Discovery", "potential_impact": 75, "infrastructure_readiness": 15, "gap": 60},
    {"application": "Predictive Analytics", "potential_impact": 80, "infrastructure_readiness": 30, "gap": 50},
    {"application": "Telemedicine", "potential_impact": 90, "infrastructure_readiness": 35, "gap": 55},
    {"application": "Health Records Digitization", "potential_impact": 70, "infrastructure_readiness": 40, "gap": 30}
  ]
};

// Chart colors
const colors = ['#1FB8CD', '#FFC185', '#B4413C', '#ECEBD5', '#5D878F', '#DB4545', '#D2BA4C', '#964325', '#944454', '#13343B'];

// Color mapping function
function getColorByContinent(continent) {
  switch(continent) {
    case 'North America': return '#1FB8CD';
    case 'Developed': case 'Europe': case 'Asia': return '#FFC185';
    case 'Global': case 'Standard': return '#5D878F';
    case 'Africa': case 'Americas': return '#B4413C';
    default: return '#ECEBD5';
  }
}

function getColorByRegion(region) {
  switch(region) {
    case 'North America': case 'Asia': case 'Europe': return '#1FB8CD';
    case 'Global': return '#5D878F';
    case 'Africa': return '#B4413C';
    default: return '#ECEBD5';
  }
}

// Common tooltip configuration
const commonTooltipConfig = {
  backgroundColor: 'rgba(0, 0, 0, 0.9)',
  titleColor: '#ffffff',
  bodyColor: '#ffffff',
  borderColor: '#1FB8CD',
  borderWidth: 1,
  cornerRadius: 8,
  displayColors: false,
  titleFont: {
    size: 14,
    weight: 'bold'
  },
  bodyFont: {
    size: 13
  }
};

// Animation delays for progressive reveal
let animationDelay = 0;
let isHealthcareFocus = false;

// Original healthcare chart functions
function createSpendingChart() {
  const ctx = document.getElementById('spendingChart').getContext('2d');
  
  const chartData = data.spending_comparison.map(item => ({
    label: item.region,
    value: item.spending,
    color: getColorByContinent(item.continent)
  }));

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: chartData.map(item => item.label),
      datasets: [{
        label: 'Healthcare Spending ($USD per capita)',
        data: chartData.map(item => item.value),
        backgroundColor: chartData.map(item => item.color),
        borderColor: chartData.map(item => item.color),
        borderWidth: 2,
        borderRadius: 8,
        borderSkipped: false,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        intersect: false,
        mode: 'index'
      },
      animation: {
        duration: 2000,
        delay: (context) => context.dataIndex * 200 + animationDelay,
        easing: 'easeOutBounce'
      },
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          ...commonTooltipConfig,
          callbacks: {
            title: function(context) {
              return context[0].label;
            },
            label: function(context) {
              return `$${context.parsed.y.toLocaleString()} per capita`;
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          grid: {
            color: 'rgba(255, 255, 255, 0.1)'
          },
          ticks: {
            color: '#fff',
            callback: function(value) {
              return '$' + value.toLocaleString();
            }
          }
        },
        x: {
          grid: {
            display: false
          },
          ticks: {
            color: '#fff',
            maxRotation: 45
          }
        }
      }
    }
  });
  animationDelay += 500;
}

function createWorkersChart() {
  const ctx = document.getElementById('workersChart').getContext('2d');
  
  const chartData = data.workers_comparison.map(item => ({
    label: item.region,
    value: item.workers,
    color: getColorByContinent(item.continent)
  }));

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: chartData.map(item => item.label),
      datasets: [{
        label: 'Healthcare Workers per 1,000 people',
        data: chartData.map(item => item.value),
        backgroundColor: chartData.map(item => item.color),
        borderColor: chartData.map(item => item.color),
        borderWidth: 2,
        borderRadius: 8,
        borderSkipped: false,
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        intersect: false,
        mode: 'index'
      },
      animation: {
        duration: 1800,
        delay: (context) => context.dataIndex * 150 + animationDelay,
        easing: 'easeOutQuart'
      },
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          ...commonTooltipConfig,
          callbacks: {
            title: function(context) {
              return context[0].label;
            },
            label: function(context) {
              return `${context.parsed.x} healthcare workers per 1,000 people`;
            }
          }
        }
      },
      scales: {
        x: {
          beginAtZero: true,
          grid: {
            color: 'rgba(255, 255, 255, 0.1)'
          },
          ticks: {
            color: '#fff'
          }
        },
        y: {
          grid: {
            display: false
          },
          ticks: {
            color: '#fff'
          }
        }
      }
    }
  });
  animationDelay += 500;
}

function createBurdenChart() {
  const ctx = document.getElementById('burdenChart').getContext('2d');
  
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Disease Burden', 'Healthcare Workers'],
      datasets: [{
        label: 'Africa\'s Share (%)',
        data: [25, 3],
        backgroundColor: ['#B4413C', '#DB4545'],
        borderColor: ['#B4413C', '#DB4545'],
        borderWidth: 3,
        borderRadius: 12,
        borderSkipped: false,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        intersect: false,
        mode: 'index'
      },
      animation: {
        duration: 2500,
        delay: animationDelay,
        easing: 'easeOutElastic'
      },
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          ...commonTooltipConfig,
          callbacks: {
            title: function(context) {
              return `Africa's ${context[0].label}`;
            },
            label: function(context) {
              return `${context.parsed.y}% of global total`;
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          max: 30,
          grid: {
            color: 'rgba(255, 255, 255, 0.1)'
          },
          ticks: {
            color: '#fff',
            callback: function(value) {
              return value + '%';
            }
          }
        },
        x: {
          grid: {
            display: false
          },
          ticks: {
            color: '#fff',
            font: {
              size: 14,
              weight: 'bold'
            }
          }
        }
      }
    }
  });
  animationDelay += 500;
}

function createBedsChart() {
  const ctx = document.getElementById('bedsChart').getContext('2d');
  
  const chartData = data.hospital_beds.map(item => ({
    label: item.region,
    value: item.beds,
    color: getColorByContinent(item.continent)
  }));

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: chartData.map(item => item.label),
      datasets: [{
        label: 'Hospital Beds per 1,000 people',
        data: chartData.map(item => item.value),
        backgroundColor: chartData.map(item => item.color),
        borderColor: chartData.map(item => item.color),
        borderWidth: 2,
        borderRadius: 8,
        borderSkipped: false,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        intersect: false,
        mode: 'index'
      },
      animation: {
        duration: 2000,
        delay: (context) => context.dataIndex * 180 + animationDelay,
        easing: 'easeOutBack'
      },
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          ...commonTooltipConfig,
          callbacks: {
            title: function(context) {
              return context[0].label;
            },
            label: function(context) {
              return `${context.parsed.y} hospital beds per 1,000 people`;
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          grid: {
            color: 'rgba(255, 255, 255, 0.1)'
          },
          ticks: {
            color: '#fff'
          }
        },
        x: {
          grid: {
            display: false
          },
          ticks: {
            color: '#fff',
            maxRotation: 45
          }
        }
      }
    }
  });
  animationDelay += 500;
}

function createAfricanDetailChart() {
  const ctx = document.getElementById('africanDetailChart').getContext('2d');
  
  const categoryColors = {
    'High': '#1FB8CD',
    'Medium': '#FFC185', 
    'Low': '#D2BA4C',
    'Very Low': '#B4413C'
  };

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: data.african_spending_detail.map(item => item.country),
      datasets: [{
        label: 'Healthcare Spending ($USD per capita)',
        data: data.african_spending_detail.map(item => item.spending),
        backgroundColor: data.african_spending_detail.map(item => categoryColors[item.category]),
        borderColor: data.african_spending_detail.map(item => categoryColors[item.category]),
        borderWidth: 2,
        borderRadius: 8,
        borderSkipped: false,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        intersect: false,
        mode: 'index'
      },
      animation: {
        duration: 2200,
        delay: (context) => context.dataIndex * 120 + animationDelay,
        easing: 'easeOutCubic'
      },
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          ...commonTooltipConfig,
          callbacks: {
            title: function(context) {
              return context[0].label;
            },
            label: function(context) {
              const category = data.african_spending_detail[context.dataIndex].category;
              return [`$${context.parsed.y} per capita`, `Category: ${category}`];
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          grid: {
            color: 'rgba(255, 255, 255, 0.1)'
          },
          ticks: {
            color: '#fff',
            callback: function(value) {
              return '$' + value;
            }
          }
        },
        x: {
          grid: {
            display: false
          },
          ticks: {
            color: '#fff',
            maxRotation: 45
          }
        }
      }
    }
  });
  animationDelay += 500;
}

function createProjectionChart() {
  const ctx = document.getElementById('projectionChart').getContext('2d');
  
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: data.shortage_projection.map(item => item.year.toString()),
      datasets: [{
        label: 'Healthcare Worker Shortage (Millions)',
        data: data.shortage_projection.map(item => item.shortage),
        borderColor: '#B4413C',
        backgroundColor: 'rgba(180, 65, 60, 0.2)',
        borderWidth: 4,
        fill: true,
        tension: 0.4,
        pointBackgroundColor: '#B4413C',
        pointBorderColor: '#fff',
        pointBorderWidth: 3,
        pointRadius: 8,
        pointHoverRadius: 12
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        intersect: false,
        mode: 'index'
      },
      animation: {
        duration: 2000,
        delay: animationDelay,
        easing: 'easeInOutQuart'
      },
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          ...commonTooltipConfig,
          callbacks: {
            title: function(context) {
              return `Year ${context[0].label}`;
            },
            label: function(context) {
              return `${context.parsed.y}M healthcare workers shortage`;
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          grid: {
            color: 'rgba(255, 255, 255, 0.1)'
          },
          ticks: {
            color: '#fff',
            callback: function(value) {
              return value + 'M';
            }
          }
        },
        x: {
          grid: {
            color: 'rgba(255, 255, 255, 0.1)'
          },
          ticks: {
            color: '#fff',
            font: {
              size: 14,
              weight: 'bold'
            }
          }
        }
      }
    }
  });
}

// New AI Infrastructure Chart Functions

function createDigitalDivideChart() {
  const ctx = document.getElementById('digitalDivideChart').getContext('2d');
  
  const metrics = ['Internet\nPenetration', 'Reliable\nElectricity', 'Broadband\nPenetration', '5G\nCoverage'];
  const africaData = [38, 43, 12, 11];
  const globalData = [68, 78, 62, 35];
  const developedData = [85, 95, 80, 70];

  new Chart(ctx, {
    type: 'radar',
    data: {
      labels: metrics,
      datasets: [{
        label: 'Africa',
        data: africaData,
        borderColor: '#B4413C',
        backgroundColor: 'rgba(180, 65, 60, 0.2)',
        borderWidth: 3,
        pointBackgroundColor: '#B4413C',
        pointBorderColor: '#fff',
        pointRadius: 6,
        pointHoverRadius: 10
      }, {
        label: 'Global Average',
        data: globalData,
        borderColor: '#5D878F',
        backgroundColor: 'rgba(93, 135, 143, 0.1)',
        borderWidth: 2,
        pointBackgroundColor: '#5D878F',
        pointBorderColor: '#fff',
        pointRadius: 5,
        pointHoverRadius: 8
      }, {
        label: 'Developed Nations',
        data: developedData,
        borderColor: '#1FB8CD',
        backgroundColor: 'rgba(31, 184, 205, 0.1)',
        borderWidth: 2,
        pointBackgroundColor: '#1FB8CD',
        pointBorderColor: '#fff',
        pointRadius: 5,
        pointHoverRadius: 8
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        intersect: true,
        mode: 'point'
      },
      scales: {
        r: {
          min: 0,
          max: 100,
          ticks: {
            stepSize: 25,
            color: '#fff',
            backdropColor: 'transparent'
          },
          grid: {
            color: 'rgba(255, 255, 255, 0.2)'
          },
          angleLines: {
            color: 'rgba(255, 255, 255, 0.2)'
          },
          pointLabels: {
            color: '#fff',
            font: {
              size: 12,
              weight: 'bold'
            }
          }
        }
      },
      plugins: {
        legend: {
          labels: {
            color: '#fff',
            font: {
              size: 14
            }
          }
        },
        tooltip: {
          ...commonTooltipConfig,
          callbacks: {
            title: function(context) {
              return context[0].label.replace('\n', ' ');
            },
            label: function(context) {
              return `${context.dataset.label}: ${context.parsed.r}%`;
            }
          }
        }
      }
    }
  });
}

function createSkillsGapChart() {
  const ctx = document.getElementById('skillsGapChart').getContext('2d');
  
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Digital Skills Index', 'Children with Digital Skills (%)', 'Digital Job Readiness (%)'],
      datasets: [{
        label: 'Africa',
        data: [3.4, 10, 23],
        backgroundColor: '#B4413C',
        borderColor: '#B4413C',
        borderWidth: 2,
        borderRadius: 8
      }, {
        label: 'Global Average',
        data: [6.0, 60, 45],
        backgroundColor: '#5D878F',
        borderColor: '#5D878F',
        borderWidth: 2,
        borderRadius: 8
      }, {
        label: 'Developed Nations',
        data: [8.2, 85, 72],
        backgroundColor: '#1FB8CD',
        borderColor: '#1FB8CD',
        borderWidth: 2,
        borderRadius: 8
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          labels: {
            color: '#fff',
            font: {
              size: 14
            }
          }
        },
        tooltip: {
          ...commonTooltipConfig,
          callbacks: {
            title: function(context) {
              return context[0].label;
            },
            label: function(context) {
              const suffix = context.label.includes('Index') ? '' : '%';
              return `${context.dataset.label}: ${context.parsed.y}${suffix}`;
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          grid: {
            color: 'rgba(255, 255, 255, 0.1)'
          },
          ticks: {
            color: '#fff'
          }
        },
        x: {
          grid: {
            display: false
          },
          ticks: {
            color: '#fff',
            maxRotation: 45
          }
        }
      }
    }
  });
}

function createRegulatoryChart() {
  const ctx = document.getElementById('regulatoryChart').getContext('2d');
  
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['AI Strategies\n(countries)', 'Data Protection Laws\n(% countries)', 'AI Ethics Frameworks\n(% countries)', 'Advanced ICT Reg.\n(% countries)'],
      datasets: [{
        label: 'Africa',
        data: [8, 35, 15, 18],
        backgroundColor: '#B4413C',
        borderColor: '#B4413C',
        borderWidth: 2,
        borderRadius: 8
      }, {
        label: 'Global Average',
        data: [25, 75, 45, 38],
        backgroundColor: '#5D878F',
        borderColor: '#5D878F',
        borderWidth: 2,
        borderRadius: 8
      }, {
        label: 'Developed Nations',
        data: [35, 95, 80, 65],
        backgroundColor: '#1FB8CD',
        borderColor: '#1FB8CD',
        borderWidth: 2,
        borderRadius: 8
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          labels: {
            color: '#fff',
            font: {
              size: 14
            }
          }
        },
        tooltip: {
          ...commonTooltipConfig,
          callbacks: {
            title: function(context) {
              return context[0].label.replace('\n', ' ');
            },
            label: function(context) {
              const isCountries = context.label.includes('countries)');
              const suffix = isCountries ? ' countries' : '%';
              return `${context.dataset.label}: ${context.parsed.y}${suffix}`;
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          grid: {
            color: 'rgba(255, 255, 255, 0.1)'
          },
          ticks: {
            color: '#fff'
          }
        },
        x: {
          grid: {
            display: false
          },
          ticks: {
            color: '#fff',
            maxRotation: 0,
            font: {
              size: 11
            }
          }
        }
      }
    }
  });
}

function createEconomicGapChart() {
  const ctx = document.getElementById('economicGapChart').getContext('2d');
  
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['VC Funding per Capita ($)', 'R&D Spending (% GDP)', 'Tech Startup Density', 'Tech Unicorns (scaled)'],
      datasets: [{
        label: 'Africa',
        data: [1.8, 0.3, 2.3, 0.1],
        backgroundColor: '#B4413C',
        borderColor: '#B4413C',
        borderWidth: 3,
        borderRadius: 10
      }, {
        label: 'Global Average',
        data: [45, 2.4, 8.7, 5],
        backgroundColor: '#5D878F',
        borderColor: '#5D878F',
        borderWidth: 2,
        borderRadius: 8
      }, {
        label: 'United States',
        data: [180, 3.5, 15.4, 60],
        backgroundColor: '#1FB8CD',
        borderColor: '#1FB8CD',
        borderWidth: 2,
        borderRadius: 8
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          labels: {
            color: '#fff',
            font: {
              size: 14
            }
          }
        },
        tooltip: {
          ...commonTooltipConfig,
          callbacks: {
            title: function(context) {
              return context[0].label;
            },
            label: function(context) {
              const metric = context.label;
              let suffix = '';
              if (metric.includes('$')) suffix = '$';
              else if (metric.includes('%')) suffix = '%';
              else if (metric.includes('scaled')) suffix = ' (scaled)';
              return `${context.dataset.label}: ${context.parsed.y}${suffix}`;
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          grid: {
            color: 'rgba(255, 255, 255, 0.1)'
          },
          ticks: {
            color: '#fff'
          }
        },
        x: {
          grid: {
            display: false
          },
          ticks: {
            color: '#fff',
            maxRotation: 45,
            font: {
              size: 11
            }
          }
        }
      }
    }
  });
}

function createReadinessScoresChart() {
  const ctx = document.getElementById('readinessScoresChart').getContext('2d');
  
  const chartData = aiData.ai_readiness_scores.map(item => ({
    label: item.country,
    value: item.score,
    color: getColorByRegion(item.region)
  }));

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: chartData.map(item => item.label),
      datasets: [{
        label: 'AI Readiness Score',
        data: chartData.map(item => item.value),
        backgroundColor: chartData.map(item => item.color),
        borderColor: chartData.map(item => item.color),
        borderWidth: 2,
        borderRadius: 8
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          ...commonTooltipConfig,
          callbacks: {
            title: function(context) {
              return context[0].label;
            },
            label: function(context) {
              return `AI Readiness Score: ${context.parsed.x}/100`;
            }
          }
        }
      },
      scales: {
        x: {
          beginAtZero: true,
          max: 100,
          grid: {
            color: 'rgba(255, 255, 255, 0.1)'
          },
          ticks: {
            color: '#fff'
          }
        },
        y: {
          grid: {
            display: false
          },
          ticks: {
            color: '#fff'
          }
        }
      }
    }
  });
}

function createOpportunityGapChart() {
  const ctx = document.getElementById('opportunityGapChart').getContext('2d');
  
  const chartData = aiData.healthcare_ai_potential.map(item => ({
    x: item.infrastructure_readiness,
    y: item.potential_impact,
    label: item.application
  }));

  new Chart(ctx, {
    type: 'scatter',
    data: {
      datasets: [{
        label: 'Healthcare AI Applications',
        data: chartData,
        backgroundColor: '#B4413C',
        borderColor: '#DB4545',
        borderWidth: 3,
        pointRadius: 12,
        pointHoverRadius: 16
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        intersect: true,
        mode: 'point'
      },
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          ...commonTooltipConfig,
          filter: function(tooltipItem) {
            return tooltipItem.datasetIndex === 0;
          },
          callbacks: {
            title: function(context) {
              return context[0].raw.label;
            },
            label: function(context) {
              return [
                `Potential Impact: ${context.parsed.y}%`,
                `Infrastructure Readiness: ${context.parsed.x}%`,
                `Gap: ${context.parsed.y - context.parsed.x} points`
              ];
            }
          }
        }
      },
      scales: {
        x: {
          title: {
            display: true,
            text: 'Infrastructure Readiness (%)',
            color: '#fff',
            font: {
              size: 14,
              weight: 'bold'
            }
          },
          min: 0,
          max: 100,
          grid: {
            color: 'rgba(255, 255, 255, 0.1)'
          },
          ticks: {
            color: '#fff'
          }
        },
        y: {
          title: {
            display: true,
            text: 'Potential Impact (%)',
            color: '#fff',
            font: {
              size: 14,
              weight: 'bold'
            }
          },
          min: 0,
          max: 100,
          grid: {
            color: 'rgba(255, 255, 255, 0.1)'
          },
          ticks: {
            color: '#fff'
          }
        }
      }
    }
  });
}

// Toggle functionality
function setupToggle() {
  const toggle = document.getElementById('healthcareToggle');
  toggle.addEventListener('change', function() {
    isHealthcareFocus = this.checked;
    // Update charts based on toggle state
    updateChartsForFilter();
  });
}

function updateChartsForFilter() {
  // This would update chart data based on healthcare focus
  // For now, we'll just log the state change
  console.log('Healthcare focus:', isHealthcareFocus);
}

// Initialize all charts when page loads
document.addEventListener('DOMContentLoaded', function() {
  // Add entrance animations to chart sections
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('chart-animate-in');
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.chart-section').forEach((section) => {
    observer.observe(section);
  });

  // Initialize healthcare charts with staggered delays
  setTimeout(createSpendingChart, 500);
  setTimeout(createWorkersChart, 1000);
  setTimeout(createBurdenChart, 1500);
  setTimeout(createBedsChart, 2000);
  setTimeout(createAfricanDetailChart, 2500);
  setTimeout(createProjectionChart, 3000);
  
  // Initialize AI infrastructure charts
  setTimeout(createDigitalDivideChart, 3500);
  setTimeout(createSkillsGapChart, 4000);
  setTimeout(createRegulatoryChart, 4500);
  setTimeout(createEconomicGapChart, 5000);
  setTimeout(createReadinessScoresChart, 5500);
  setTimeout(createOpportunityGapChart, 6000);
  
  // Setup toggle functionality
  setupToggle();
});

// Add smooth scrolling behavior
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({
        behavior: 'smooth'
      });
    }
  });
});