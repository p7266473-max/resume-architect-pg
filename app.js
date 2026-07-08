/* ==========================================================================
   Resume Architect PG - Core Application & Rendering Logic
   ========================================================================== */

// Profile Configuration Data
const profileConfigs = {
    mba: {
        label: "MBA Specialization",
        specializations: [
            { id: "finance", name: "Finance & Investment Banking" },
            { id: "marketing", name: "Marketing & Brand Strategy" },
            { id: "hr", name: "Human Resource Management" },
            { id: "operations", name: "Operations & Supply Chain" },
            { id: "systems", name: "Systems & Business Analytics" }
        ],
        suggestions: {
            finance: {
                title: "MBA Candidate | Finance & Investment Banking",
                summary: "Analytical MBA candidate with a strong foundation in corporate finance, financial modeling, and investment banking principles. Proficient in performing company valuations using DCF and Comparable Company Analysis (CCA). Adept at translating complex financial data into strategic recommendations to optimize capital budgeting.",
                bullets: [
                    "Constructed detailed three-statement financial models and projected future cash flows for valuations.",
                    "Analyzed capital structure optimization strategies, improving theoretical cost of capital by 40bps.",
                    "Conducted risk assessment reports for M&A scenarios, evaluating strategic synergies and premium pricing."
                ]
            },
            marketing: {
                title: "MBA Candidate | Marketing & Brand Strategy",
                summary: "Creative and analytical MBA specializing in Marketing and Brand Management. Experienced in conducting customer acquisition cost (CAC) analyses, customer journey mapping, and digital campaign planning. Skilled at leveraging data analytics to craft high-conversion product positioning strategies.",
                bullets: [
                    "Designed and executed comprehensive market research surveys, identifying key growth segments.",
                    "Formulated a go-to-market (GTM) strategy for a digital product launch, boosting target conversions by 15%.",
                    "Optimized social media campaign budgets, reducing overall customer acquisition cost (CAC) by 18%."
                ]
            },
            hr: {
                title: "MBA Candidate | Human Resource Management",
                summary: "People-centric MBA candidate specializing in Strategic Human Resources and Organizational Development. Proficient in designing talent acquisition pipelines, performance appraisal frameworks, and employee engagement programs. Committed to building diverse and high-performing workplace cultures.",
                bullets: [
                    "Formulated structured competency mapping models for technical profiles, aligning hiring with corporate objectives.",
                    "Redesigned the onboarding workflow, reducing the employee attrition rate by 12% in the first quarter.",
                    "Analyzed annual performance appraisal data to identify training needs and gaps across core departments."
                ]
            },
            operations: {
                title: "MBA Candidate | Operations & Supply Chain",
                summary: "Process-oriented MBA candidate specializing in Operations Management and Logistics. Proficient in Six Sigma methodologies, bottleneck identification, and lean supply chain principles. Skilled in leveraging linear programming models to optimize distribution networks.",
                bullets: [
                    "Mapped warehouse layouts and logistics workflows, enhancing daily order fulfillment speeds by 22%.",
                    "Managed inventory optimization audits using ABC analysis, reducing carrying costs by 15%.",
                    "Applied Lean principles to operational pipelines, eliminating redundant processing steps for faster delivery."
                ]
            },
            systems: {
                title: "MBA Candidate | Systems & Business Analytics",
                summary: "Data-driven MBA candidate specializing in Business Analytics and Systems Management. Skilled in translating complex database inputs into readable business intelligence dashboards. Proficient in SQL, Tableau, and applying predictive analytical algorithms.",
                bullets: [
                    "Developed dynamic Tableau dashboards tracking key operational KPIs, cutting weekly reporting time by 10 hours.",
                    "Formulated predictive customer churn models using regression analysis to support retention programs.",
                    "Coordinated cross-functional IT projects, managing sprints and product backlogs under Agile scrum methodologies."
                ]
            }
        }
    },
    ug: {
        label: "Undergraduate Degree",
        specializations: [
            { id: "cs", name: "B.Tech/B.E - Computer Science & IT" },
            { id: "commerce", name: "B.Com - Commerce & Accounting" },
            { id: "science", name: "B.Sc - General Sciences" },
            { id: "arts", name: "B.A - Humanities & Arts" },
            { id: "bba", name: "BBA - Business Administration" }
        ],
        suggestions: {
            cs: {
                title: "Software Engineering Undergraduate",
                summary: "Aspiring Software Engineer and Undergraduate student in Computer Science. Proficient in full-stack development, algorithms, and database management systems. Experienced in building scalable web solutions using modern programming architectures.",
                bullets: [
                    "Designed and implemented RESTful APIs using Node.js and Express, enhancing backend scalability.",
                    "Developed a fully responsive web application with React.js, improving average user engagement times.",
                    "Optimized database queries in MySQL, reducing average load times by 20% on production systems."
                ]
            },
            commerce: {
                title: "B.Com Candidate | Accounting & Finance",
                summary: "Detail-oriented Bachelor of Commerce student with solid knowledge in accounting principles, taxation guidelines, and corporate finance laws. Proficient in Tally ERP, Excel modeling, and preparing financial audit summaries.",
                bullets: [
                    "Maintained ledger accounts and prepared general financial balance sheets for quarterly reviews.",
                    "Assisted in reviewing tax compliance worksheets, identifying opportunities for deduplication.",
                    "Conducted basic ratio analysis to assess liquidity and financial health of case study projects."
                ]
            },
            science: {
                title: "B.Sc Undergraduate | Research & Data Analytics",
                summary: "Methodical Bachelor of Science undergraduate with experience in statistical computing and data modeling. Proficient in running experimental trials, analyzing data arrays, and writing structured research reports.",
                bullets: [
                    "Conducted structured statistical analysis on laboratory datasets using R programming and Python.",
                    "Authored research reports detailing chemical properties and presenting data trends in visual graphs.",
                    "Coordinated laboratory safety guidelines, ensuring compliance with academic protocols."
                ]
            },
            arts: {
                title: "B.A Undergraduate | Communications & Writing",
                summary: "Creative Humanities and Arts student specializing in communication systems, media writing, and research methodology. Proficient in content creation, editing, and executing structured qualitative studies.",
                bullets: [
                    "Published articles in the university newsletter, increasing student engagement by 25%.",
                    "Conducted qualitative field research surveys, presenting analytical findings at local student symposiums.",
                    "Managed social media copy and communication logs for student-led activities and events."
                ]
            },
            bba: {
                title: "BBA Undergraduate | Management & Strategy",
                summary: "Proactive Business Administration student with a foundation in sales strategy, project management, and business communication. Skilled in organizing campus-wide events and pitching client proposals.",
                bullets: [
                    "Managed marketing budgets for the annual college fest, securing corporate sponsorships of $5k+.",
                    "Led a student task force of 12 peers to execute community service initiatives.",
                    "Coordinated product pitch decks for business competition presentations, winning top ranks."
                ]
            }
        }
    }
};

// Application State Model
let appState = {
    profileType: "mba", // 'mba' or 'ug'
    specialization: "finance",
    template: "modern",
    fullname: "",
    title: "",
    email: "",
    phone: "",
    location: "",
    linkedin: "",
    github: "",
    summary: "",
    education: [],
    experience: [],
    projects: [],
    skillsCore: "",
    skillsTools: "",
    certs: "",
    awards: ""
};

// DOM References
const dom = {
    profileTypeMba: document.querySelector('input[value="mba"]'),
    profileTypeUg: document.querySelector('input[value="ug"]'),
    labelMba: document.getElementById('label-mba'),
    labelUg: document.getElementById('label-ug'),
    specLabel: document.getElementById('spec-label'),
    specDropdown: document.getElementById('spec-dropdown'),
    templateButtons: document.querySelectorAll('.tmpl-btn'),
    resumePreview: document.getElementById('resume-preview'),
    
    // Inputs
    fullname: document.getElementById('input-fullname'),
    title: document.getElementById('input-title'),
    email: document.getElementById('input-email'),
    phone: document.getElementById('input-phone'),
    location: document.getElementById('input-location'),
    linkedin: document.getElementById('input-linkedin'),
    github: document.getElementById('input-github'),
    summary: document.getElementById('input-summary'),
    skillsCore: document.getElementById('input-skills-core'),
    skillsTools: document.getElementById('input-skills-tools'),
    certs: document.getElementById('input-certs'),
    awards: document.getElementById('input-awards'),
    
    // Dynamic List Containers
    educationList: document.getElementById('education-list'),
    experienceList: document.getElementById('experience-list'),
    projectsList: document.getElementById('projects-list'),
    
    // Core Control Buttons
    btnAddEducation: document.getElementById('btn-add-education'),
    btnAddExperience: document.getElementById('btn-add-experience'),
    btnAddProject: document.getElementById('btn-add-project'),
    btnExport: document.getElementById('btn-export'),
    btnLoadSample: document.getElementById('btn-load-sample'),
    btnReset: document.getElementById('btn-reset'),
    btnApplySummarySuggest: document.getElementById('btn-apply-summary-suggest')
};

/* Initialize Event Listeners */
function init() {
    // Category Switcher
    dom.profileTypeMba.addEventListener('change', () => handleCategoryChange('mba'));
    dom.profileTypeUg.addEventListener('change', () => handleCategoryChange('ug'));
    dom.labelMba.addEventListener('click', () => { dom.profileTypeMba.checked = true; handleCategoryChange('mba'); });
    dom.labelUg.addEventListener('click', () => { dom.profileTypeUg.checked = true; handleCategoryChange('ug'); });

    // Specialization Dropdown
    dom.specDropdown.addEventListener('change', (e) => {
        appState.specialization = e.target.value;
        saveState();
        renderPreview();
    });

    // Design Template Selectors
    dom.templateButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            dom.templateButtons.forEach(b => b.classList.remove('active'));
            const target = e.currentTarget;
            target.classList.add('active');
            appState.template = target.getAttribute('data-template');
            
            // Update preview template classes
            dom.resumePreview.className = `a4-page template-${appState.template}`;
            saveState();
        });
    });

    // Form dynamic input bindings
    const inputs = ['fullname', 'title', 'email', 'phone', 'location', 'linkedin', 'github', 'summary', 'skillsCore', 'skillsTools', 'certs', 'awards'];
    inputs.forEach(field => {
        dom[field].addEventListener('input', (e) => {
            appState[field] = e.target.value;
            saveState();
            renderPreview();
        });
    });

    // Dynamic Lists Actions
    dom.btnAddEducation.addEventListener('click', () => addListEntry('education'));
    dom.btnAddExperience.addEventListener('click', () => addListEntry('experience'));
    dom.btnAddProject.addEventListener('click', () => addListEntry('projects'));

    // Top Level Control Actions
    dom.btnApplySummarySuggest.addEventListener('click', applyAISuggestion);
    dom.btnLoadSample.addEventListener('click', loadSampleDataset);
    dom.btnReset.addEventListener('click', resetApplication);
    dom.btnExport.addEventListener('click', () => window.print());

    // Setup initial specialization options
    updateSpecializationDropdown();
    
    // Load from LocalStorage if exists
    loadState();
}

/* Category State Manager */
function handleCategoryChange(type) {
    appState.profileType = type;
    if (type === 'mba') {
        dom.labelMba.classList.add('active');
        dom.labelUg.classList.remove('active');
        dom.specLabel.textContent = "MBA Specialization";
    } else {
        dom.labelUg.classList.add('active');
        dom.labelMba.classList.remove('active');
        dom.specLabel.textContent = "Undergraduate Degree";
    }
    updateSpecializationDropdown();
    
    // Reset specialization to first entry in category list
    appState.specialization = profileConfigs[type].specializations[0].id;
    dom.specDropdown.value = appState.specialization;
    
    saveState();
    renderPreview();
}

/* Update Dropdown UI options */
function updateSpecializationDropdown() {
    const list = profileConfigs[appState.profileType].specializations;
    dom.specDropdown.innerHTML = '';
    list.forEach(item => {
        const option = document.createElement('option');
        option.value = item.id;
        option.textContent = item.name;
        dom.specDropdown.appendChild(option);
    });
}

/* AI Objective Suggestion Manager */
function applyAISuggestion() {
    const category = appState.profileType;
    const spec = appState.specialization;
    const data = profileConfigs[category].suggestions[spec];
    if (data) {
        appState.title = data.title;
        appState.summary = data.summary;
        
        dom.title.value = appState.title;
        dom.summary.value = appState.summary;
        
        saveState();
        renderPreview();
    }
}

/* Dynamic list managers */
function addListEntry(type, defaultValues = null) {
    const id = Date.now().toString() + Math.random().toString(36).substr(2, 5);
    const item = defaultValues ? { id, ...defaultValues } : createEmptyListEntry(type, id);
    
    appState[type].push(item);
    renderListUI(type);
    saveState();
    renderPreview();
}

function createEmptyListEntry(type, id) {
    if (type === 'education') {
        return { id, degree: "", school: "", location: "", gpa: "", year: "" };
    } else if (type === 'experience') {
        return { id, role: "", company: "", duration: "", details: "" };
    } else if (type === 'projects') {
        return { id, title: "", tech: "", details: "" };
    }
}

function deleteListEntry(type, id) {
    appState[type] = appState[type].filter(item => item.id !== id);
    renderListUI(type);
    saveState();
    renderPreview();
}

function handleListInput(type, id, field, value) {
    const item = appState[type].find(item => item.id === id);
    if (item) {
        item[field] = value;
        saveState();
        renderPreview();
    }
}

/* UI render lists */
function renderListUI(type) {
    const container = dom[`${type}List`];
    container.innerHTML = '';
    
    appState[type].forEach(item => {
        const div = document.createElement('div');
        div.className = 'dynamic-item';
        div.innerHTML = `<button class="item-delete-btn" data-id="${item.id}"><i class="fa-solid fa-xmark"></i></button>`;
        
        if (type === 'education') {
            div.appendChild(createInputElement('Degree/Major', 'degree', item, type));
            div.appendChild(createInputElement('School/University', 'school', item, type));
            div.appendChild(createInputElement('GPA/Grade', 'gpa', item, type));
            div.appendChild(createInputElement('Completion Year', 'year', item, type));
        } else if (type === 'experience') {
            div.appendChild(createInputElement('Job Role', 'role', item, type));
            div.appendChild(createInputElement('Company Name', 'company', item, type));
            div.appendChild(createInputElement('Duration (e.g. June 2023 - Present)', 'duration', item, type));
            div.appendChild(createTextareaElement('Work Details / Bullet Points (one per line)', 'details', item, type));
        } else if (type === 'projects') {
            div.appendChild(createInputElement('Project Title', 'title', item, type));
            div.appendChild(createInputElement('Technologies Used', 'tech', item, type));
            div.appendChild(createTextareaElement('Key Details / Achievements (one per line)', 'details', item, type));
        }
        
        container.appendChild(div);
        
        // Bind delete action
        div.querySelector('.item-delete-btn').addEventListener('click', () => deleteListEntry(type, item.id));
    });
}

function createInputElement(label, field, item, type) {
    const group = document.createElement('div');
    group.className = 'input-group';
    group.innerHTML = `
        <label>${label}</label>
        <input type="text" value="${item[field] || ''}">
    `;
    group.querySelector('input').addEventListener('input', (e) => handleListInput(type, item.id, field, e.target.value));
    return group;
}

function createTextareaElement(label, field, item, type) {
    const group = document.createElement('div');
    group.className = 'input-group full-width';
    group.innerHTML = `
        <label>${label}</label>
        <textarea rows="3">${item[field] || ''}</textarea>
    `;
    group.querySelector('textarea').addEventListener('input', (e) => handleListInput(type, item.id, field, e.target.value));
    return group;
}

/* LocalStorage Persistence managers */
function saveState() {
    localStorage.setItem('resume_architect_state', JSON.stringify(appState));
}

function loadState() {
    const data = localStorage.getItem('resume_architect_state');
    if (data) {
        try {
            appState = JSON.parse(data);
            
            // Set Category
            if (appState.profileType === 'mba') {
                dom.profileTypeMba.checked = true;
                dom.labelMba.classList.add('active');
                dom.labelUg.classList.remove('active');
                dom.specLabel.textContent = "MBA Specialization";
            } else {
                dom.profileTypeUg.checked = true;
                dom.labelUg.classList.add('active');
                dom.labelMba.classList.remove('active');
                dom.specLabel.textContent = "Undergraduate Degree";
            }
            
            updateSpecializationDropdown();
            dom.specDropdown.value = appState.specialization;
            
            // Bind template
            dom.templateButtons.forEach(btn => {
                if (btn.getAttribute('data-template') === appState.template) {
                    btn.classList.add('active');
                } else {
                    btn.classList.remove('active');
                }
            });
            dom.resumePreview.className = `a4-page template-${appState.template}`;
            
            // Set inputs
            const fields = ['fullname', 'title', 'email', 'phone', 'location', 'linkedin', 'github', 'summary', 'skillsCore', 'skillsTools', 'certs', 'awards'];
            fields.forEach(field => {
                dom[field].value = appState[field] || '';
            });
            
            // Render Dynamic lists
            renderListUI('education');
            renderListUI('experience');
            renderListUI('projects');
            
            renderPreview();
        } catch (e) {
            console.error("Failed to parse localstorage state", e);
        }
    } else {
        loadSampleDataset();
    }
}

/* Sample Dataset Creator */
function loadSampleDataset() {
    const isMba = appState.profileType === 'mba';
    const spec = appState.specialization;
    
    let sampleData = {
        fullname: "Alexander Morgan",
        email: "alex.morgan@domain.com",
        phone: "+1 (312) 442-9901",
        location: "Chicago, IL",
        linkedin: "linkedin.com/in/alexmorgan",
        github: "github.com/alexmorgan-dev"
    };
    
    // Core profile suggestions
    const suggestion = profileConfigs[appState.profileType].suggestions[spec];
    if (suggestion) {
        sampleData.title = suggestion.title;
        sampleData.summary = suggestion.summary;
    }
    
    // Education Sample Setup
    if (isMba) {
        sampleData.education = [
            { id: '1', degree: `MBA - Specialization in ${profileConfigs.mba.specializations.find(s=>s.id===spec).name}`, school: "Kellogg School of Management", location: "Evanston, IL", gpa: "3.8/4.0", year: "2026" },
            { id: '2', degree: "Bachelor of Business Administration (BBA)", school: "University of Illinois", location: "Urbana-Champaign, IL", gpa: "3.9/4.0", year: "2023" }
        ];
    } else {
        sampleData.education = [
            { id: '1', degree: profileConfigs.ug.specializations.find(s=>s.id===spec).name, school: "University of Illinois", location: "Urbana-Champaign, IL", gpa: "3.85/4.0", year: "2026" }
        ];
    }
    
    // Experience Sample Setup
    if (isMba) {
        sampleData.experience = [
            {
                id: '1',
                role: isMba && spec === 'finance' ? "Investment Analyst (Intern)" : "Business Strategy Associate",
                company: "Apex Advisory Group",
                duration: "June 2024 - August 2024",
                details: suggestion.bullets.join('\n')
            },
            {
                id: '2',
                role: "Financial Analyst / Coordinator",
                company: "Nexa Enterprises",
                duration: "June 2022 - May 2024",
                details: "Analyzed weekly operational and supply chain reports to identify performance margins.\nCoordinated communication pipelines between 4 project teams, reducing project cycle times by 10%."
            }
        ];
    } else {
        sampleData.experience = [
            {
                id: '1',
                role: spec === 'cs' ? "Junior Developer Intern" : "Business Operations Intern",
                company: "InnovateTech Corp",
                duration: "May 2025 - August 2025",
                details: suggestion.bullets.join('\n')
            }
        ];
    }
    
    // Project Samples
    if (isMba) {
        sampleData.projects = [
            {
                id: '1',
                title: "Strategic Valuation Case Study",
                tech: "Financial Models, PPT, Valuations",
                details: "Performed valuation on a hypothetical $50M takeover target using DCF model.\nDelivered the findings to a simulated Board of Directors, receiving first prize out of 15 student cases."
            }
        ];
    } else {
        sampleData.projects = [
            {
                id: '1',
                title: spec === 'cs' ? "Autonomous Web Scraper Suite" : "Regional Competitor Analysis Study",
                tech: spec === 'cs' ? "Python, BeautifulSoup, SQLite" : "Excel Analysis, Competitor Mapping",
                details: spec === 'cs' 
                    ? "Built a data crawling workflow handling 10k+ URLs, gathering consumer trends.\nPublished structured database outputs used by campus marketing organizations."
                    : "Conducted field study on local retail outlets to analyze customer footfall.\nSynthesized critical findings into a 20-page market research document."
            }
        ];
    }
    
    // Skills
    if (isMba) {
        sampleData.skillsCore = spec === 'finance' ? "Corporate Valuation, Equity Analysis, Asset Allocation" : "Strategic Planning, Brand Architecture, Market Analysis";
        sampleData.skillsTools = spec === 'finance' ? "Tally, Excel, Bloomberg Terminal" : "Tableau, PowerPoint, Google Analytics";
        sampleData.certs = "CFA Level 1 Candidate, Project Management Professional (PMP)";
        sampleData.awards = "Recipient of Dean's List Award (2024), Academic Merit Scholarship";
    } else {
        sampleData.skillsCore = spec === 'cs' ? "Algorithms, Data Structures, OOP Design" : "Tax Accounting, Ledger Entries, Financial Statements";
        sampleData.skillsTools = spec === 'cs' ? "Git, Python, JavaScript, CSS" : "Excel, QuickBooks, Google Analytics";
        sampleData.certs = spec === 'cs' ? "AWS Certified Cloud Practitioner" : "Google Project Management Certificate";
        sampleData.awards = "Winner of College Hackathon (2025), President of Science Society";
    }
    
    // Load into state and inputs
    appState = { ...appState, ...sampleData };
    
    // Update input UI elements values
    const fields = ['fullname', 'title', 'email', 'phone', 'location', 'linkedin', 'github', 'summary', 'skillsCore', 'skillsTools', 'certs', 'awards'];
    fields.forEach(field => {
        dom[field].value = appState[field] || '';
    });
    
    renderListUI('education');
    renderListUI('experience');
    renderListUI('projects');
    
    saveState();
    renderPreview();
}

/* Reset Application Data */
function resetApplication() {
    if (confirm("Are you sure you want to clear all data? This cannot be undone.")) {
        localStorage.removeItem('resume_architect_state');
        appState = {
            profileType: appState.profileType,
            specialization: appState.specialization,
            template: appState.template,
            fullname: "",
            title: "",
            email: "",
            phone: "",
            location: "",
            linkedin: "",
            github: "",
            summary: "",
            education: [],
            experience: [],
            projects: [],
            skillsCore: "",
            skillsTools: "",
            certs: "",
            awards: ""
        };
        
        // Reset Inputs UI
        const fields = ['fullname', 'title', 'email', 'phone', 'location', 'linkedin', 'github', 'summary', 'skillsCore', 'skillsTools', 'certs', 'awards'];
        fields.forEach(field => {
            dom[field].value = '';
        });
        
        renderListUI('education');
        renderListUI('experience');
        renderListUI('projects');
        
        saveState();
        renderPreview();
    }
}

/* HTML renderer for the A4 Preview Pane */
function renderPreview() {
    let html = '';
    
    // Header Render
    html += `
        <div class="p-header">
            <h1>${appState.fullname || 'Your Name'}</h1>
            ${appState.title ? `<div class="p-subtitle">${appState.title}</div>` : ''}
            <div class="p-contacts">
                ${appState.email ? `<span><i class="fa-solid fa-envelope"></i> ${appState.email}</span>` : ''}
                ${appState.phone ? `<span><i class="fa-solid fa-phone"></i> ${appState.phone}</span>` : ''}
                ${appState.location ? `<span><i class="fa-solid fa-location-dot"></i> ${appState.location}</span>` : ''}
                ${appState.linkedin ? `<span><i class="fa-brands fa-linkedin"></i> ${appState.linkedin}</span>` : ''}
                ${appState.github ? `<span><i class="fa-brands fa-github"></i> ${appState.github}</span>` : ''}
            </div>
        </div>
    `;
    
    // Professional Summary
    if (appState.summary) {
        html += `
            <div class="p-summary">
                ${appState.summary}
            </div>
        `;
    }
    
    // Education Section
    if (appState.education && appState.education.length > 0) {
        html += `<div class="preview-section">
            <div class="section-heading">Education</div>
        `;
        appState.education.forEach(edu => {
            html += `
                <div class="edu-item">
                    <div class="item-row">
                        <span>${edu.degree || 'Degree Title'}</span>
                        <span>${edu.year || ''}</span>
                    </div>
                    <div class="item-subrow">
                        <span>${edu.school || 'Institution Name'}${edu.location ? `, ${edu.location}` : ''}</span>
                        <span>${edu.gpa ? `GPA: ${edu.gpa}` : ''}</span>
                    </div>
                </div>
            `;
        });
        html += `</div>`;
    }
    
    // Experience Section
    if (appState.experience && appState.experience.length > 0) {
        html += `<div class="preview-section">
            <div class="section-heading">Professional Experience</div>
        `;
        appState.experience.forEach(exp => {
            const bulletItems = exp.details ? exp.details.split('\n').filter(b => b.trim().length > 0) : [];
            html += `
                <div class="exp-item">
                    <div class="item-row">
                        <span>${exp.role || 'Job Role'}</span>
                        <span>${exp.duration || ''}</span>
                    </div>
                    <div class="item-subrow">
                        <span>${exp.company || 'Company'}</span>
                    </div>
                    ${bulletItems.length > 0 ? `
                        <ul class="item-desc">
                            ${bulletItems.map(bullet => `<li>${bullet}</li>`).join('')}
                        </ul>
                    ` : ''}
                </div>
            `;
        });
        html += `</div>`;
    }

    // Projects Section
    if (appState.projects && appState.projects.length > 0) {
        html += `<div class="preview-section">
            <div class="section-heading">Academic & Personal Projects</div>
        `;
        appState.projects.forEach(proj => {
            const bulletItems = proj.details ? proj.details.split('\n').filter(b => b.trim().length > 0) : [];
            html += `
                <div class="proj-item">
                    <div class="item-row">
                        <span>${proj.title || 'Project Title'}</span>
                        <span>${proj.tech ? `[${proj.tech}]` : ''}</span>
                    </div>
                    ${bulletItems.length > 0 ? `
                        <ul class="item-desc">
                            ${bulletItems.map(bullet => `<li>${bullet}</li>`).join('')}
                        </ul>
                    ` : ''}
                </div>
            `;
        });
        html += `</div>`;
    }

    // Core Skills Section
    if (appState.skillsCore || appState.skillsTools) {
        html += `<div class="preview-section">
            <div class="section-heading">Skills & Competencies</div>
            <div class="skills-grid">
        `;
        if (appState.skillsCore) {
            html += `
                <span class="skills-category">Core Expertise:</span>
                <span class="skills-list">${appState.skillsCore}</span>
            `;
        }
        if (appState.skillsTools) {
            html += `
                <span class="skills-category">Tools & Technologies:</span>
                <span class="skills-list">${appState.skillsTools}</span>
            `;
        }
        html += `
            </div>
        </div>
        `;
    }

    // Certifications & Extra-curriculars Section
    if (appState.certs || appState.awards) {
        html += `<div class="preview-section">
            <div class="section-heading">Certifications & Honors</div>
            <ul class="certs-awards-list">
        `;
        if (appState.certs) {
            appState.certs.split(',').forEach(c => {
                if (c.trim()) html += `<li>${c.trim()}</li>`;
            });
        }
        if (appState.awards) {
            appState.awards.split(',').forEach(a => {
                if (a.trim()) html += `<li>${a.trim()}</li>`;
            });
        }
        html += `
            </ul>
        </div>
        `;
    }

    dom.resumePreview.innerHTML = html;
}

// Start core app on DOM load
window.addEventListener('DOMContentLoaded', init);
