select * from CovidDeaths;
select * from CovidVaccinations;


------Data we will be using

select location, date, total_cases, new_cases, total_deaths, population 
from CovidDeaths
order by 1,2;

-------Total_cases VS Total_deaths

select location, date, total_cases, total_deaths, (total_deaths*1.000/total_cases)*100 as DeathPercentage
from PortfolioProjectCovid.dbo.CovidDeaths
where location like '%India%'
order by 1,2;

--------Total_cases VS Population

select location, date, total_cases, population, (total_cases*1.000/population)*100 as CovidPopulationPercentage
from PortfolioProjectCovid.dbo.CovidDeaths
where location like '%India%'
order by 1,2;

-------Countries with highest infection rate compared to population

select location, population, MAX(total_cases) as HighestInfectionCount,MAX((total_cases*1.000/population))*100 as PercentagePopulationAffected
from PortfolioProjectCovid.dbo.CovidDeaths
--where location like '%India%'
group by location, population
order by PercentagePopulationAffected desc;

-------Highes death count per population

select location, MAX(total_deaths) as TotalDeathCount
from PortfolioProjectCovid.dbo.CovidDeaths
--where location like '%India%'
where continent is not null
group by location, population
order by TotalDeathCount desc;

-------Querying by continent & income

select continent, MAX(total_deaths) as TotalDeathCount
from PortfolioProjectCovid.dbo.CovidDeaths
--where location like '%India%'
where continent is not null
group by continent
order by TotalDeathCount desc;

select location, MAX(total_deaths) as TotalDeathCount
from PortfolioProjectCovid.dbo.CovidDeaths
--where location like '%India%'
where location like '%income%'
group by location
order by TotalDeathCount desc;

---------Global Numbers

-- Option A when divisor(new_cases) = 0 by adding a condition where not 0
select date, SUM(new_cases) as NewCasesPerDay, SUM(new_deaths) as NewDeathsPerDay, sum(new_deaths)/SUM(new_cases)*100 as DeathPercentage 
from CovidDeaths
where continent is not null and new_cases <>0
group by date
order by 1,2;

-- Option B when divisor(new_cases) = 0 by using case statement
select date, SUM(new_cases) as NewCasesPerDay, SUM(new_deaths) as NewDeathsPerDay, 
CASE
	WHEN SUM(new_cases)=0 THEN NULL
	ELSE sum(new_deaths*1.000)/SUM(new_cases)*100  
END AS DeathPercentage
--sum(new_deaths)/SUM(new_cases)*100 as DeathPercentage 
from CovidDeaths
where continent is not null and new_cases <>0
group by date
order by 1,2;

--Total cases and total deaths with percentage
select  SUM(new_cases) as NewCasesPerDay, SUM(new_deaths) as NewDeathsPerDay, sum(new_deaths*1.000)/SUM(new_cases)*100 as DeathPercentage 
from CovidDeaths
where continent is not null and new_cases <>0
--group by date
order by 1,2;



---------Total population vs new vaccinations
select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, sum(cast(vac.new_vaccinations as bigint)) over (PARTITION BY dea.location order by dea.location,  dea.date) as RollingPeopleVaccinated
from CovidDeaths dea 
join CovidVaccinations vac
on dea.location=vac.location and dea.date=vac.date
where dea.continent is not null
order by 2,3;

--Using CTE

WITH PopVSVa (Continent, Location,Date, Population, New_Vaccinations, RollingPeopleVaccinated)
AS
(
select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, sum(cast(vac.new_vaccinations as bigint)) over (PARTITION BY dea.location order by dea.location,  dea.date) as RollingPeopleVaccinated
from CovidDeaths dea 
join CovidVaccinations vac
on dea.location=vac.location and dea.date=vac.date
where dea.continent is not null
--order by 2,3
)
select *, (RollingPeopleVaccinated*1.000/Population)*100 from PopVSVa;

--Using Temp Table

Drop table if exists #PercentPeopleVaccinated
create table #PercentVaccinated 
(Continent nvarchar(20), 
Location nvarchar(35), 
Date datetime, 
Population bigint, 
NewVaccination int, 
RollingPeopleVaccinated float);

Insert into #PercentPeopleVaccinated
select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, sum(cast(vac.new_vaccinations as bigint)) over (PARTITION BY dea.location order by dea.location,  dea.date) as RollingPeopleVaccinated
from CovidDeaths dea 
join CovidVaccinations vac
on dea.location=vac.location and dea.date=vac.date
where dea.continent is not null;

select *, (RollingPeopleVaccinated*1.000/Population)*100 from #PercentPeopleVaccinated;

---------Creating Views for visualization purposes

create View PercentPeopleVaccinated as 
select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, sum(cast(vac.new_vaccinations as bigint)) over (PARTITION BY dea.location order by dea.location,  dea.date) as RollingPeopleVaccinated
from CovidDeaths dea 
join CovidVaccinations vac
on dea.location=vac.location and dea.date=vac.date
where dea.continent is not null;
