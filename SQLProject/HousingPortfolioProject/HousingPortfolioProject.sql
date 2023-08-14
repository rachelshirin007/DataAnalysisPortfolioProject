select * from [Nashville Housing Data for Data Cleaning];


---Populate property address data
select * from [Nashville Housing Data for Data Cleaning]
--where PropertyAddress is null;

select a.UniqueID, a.ParcelID, a.PropertyAddress, b.UniqueID, b.ParcelID, b.PropertyAddress, isnull(a.PropertyAddress, b.PropertyAddress) 
from [Nashville Housing Data for Data Cleaning] a
join [Nashville Housing Data for Data Cleaning] b
on a.ParcelID = b.ParcelID
and a.UniqueID <>b.UniqueID
where a.PropertyAddress is null

update a
 set PropertyAddress = isnull(a.PropertyAddress, b.PropertyAddress) 
 from [Nashville Housing Data for Data Cleaning] a
join [Nashville Housing Data for Data Cleaning] b
on a.ParcelID = b.ParcelID
and a.UniqueID <>b.UniqueID
where a.PropertyAddress is null


---Breaking address into individual columns (address, city, state)

select PropertyAddress from [Nashville Housing Data for Data Cleaning];

select CHARINDEX(',', PropertyAddress) from [Nashville Housing Data for Data Cleaning];

select PropertyAddress, SUBSTRING(PropertyAddress, 1, CHARINDEX(',', PropertyAddress) -1) as Address,
SUBSTRING(PropertyAddress, CHARINDEX(',', PropertyAddress)+1, LEN(PropertyAddress)) as City
from [Nashville Housing Data for Data Cleaning];

ALTER TABLE [Nashville Housing Data for Data Cleaning]
ADD PropertySplitAddress nvarchar(150);

select * from [Nashville Housing Data for Data Cleaning];

UPDATE [Nashville Housing Data for Data Cleaning]
set PropertySplitAddress = SUBSTRING(PropertyAddress, 1, CHARINDEX(',', PropertyAddress) -1);

ALTER TABLE [Nashville Housing Data for Data Cleaning]
ADD PropertySplitCity nvarchar(50);

select * from [Nashville Housing Data for Data Cleaning];

UPDATE [Nashville Housing Data for Data Cleaning]
set PropertySplitCity = SUBSTRING(PropertyAddress, CHARINDEX(',', PropertyAddress)+1, LEN(PropertyAddress));



select OwnerAddress from [Nashville Housing Data for Data Cleaning];

select 
PARSENAME(REPLACE(OwnerAddress, ',','.'),3) as Address,
PARSENAME(REPLACE(OwnerAddress, ',','.'),2) as City,
PARSENAME(REPLACE(OwnerAddress, ',','.'),1) as State
from [Nashville Housing Data for Data Cleaning];

ALTER TABLE [Nashville Housing Data for Data Cleaning]
ADD OwnerSplitAddress nvarchar(150);

select * from [Nashville Housing Data for Data Cleaning];

UPDATE [Nashville Housing Data for Data Cleaning]
set OwnerSplitAddress = PARSENAME(REPLACE(OwnerAddress, ',','.'),3);

ALTER TABLE [Nashville Housing Data for Data Cleaning]
ADD OwnerSplitCity nvarchar(50);

select * from [Nashville Housing Data for Data Cleaning];

UPDATE [Nashville Housing Data for Data Cleaning]
set OwnerSplitCity = PARSENAME(REPLACE(OwnerAddress, ',','.'),2);

ALTER TABLE [Nashville Housing Data for Data Cleaning]
ADD OwnerSplitState nvarchar(20);

select * from [Nashville Housing Data for Data Cleaning];

UPDATE [Nashville Housing Data for Data Cleaning]
set OwnerSplitState = PARSENAME(REPLACE(OwnerAddress, ',','.'),1);


---Change Y and N as Yes and No in SoldAsVacant

--select  distinct SoldAsVacant, count(SoldAsVacant),
select distinct SoldAsVacant2, count(SoldAsVacant2)
from [Nashville Housing Data for Data Cleaning]
group by SoldAsVacant2
order by SoldAsVacant2;

ALTER TABLE [Nashville Housing Data for Data Cleaning]
ADD SoldAsVacant2 nvarchar(5);

select * from [Nashville Housing Data for Data Cleaning];


select SoldAsVacant, 
CASE
	WHEN SoldAsVacant = 0 THEN 'No'
	WHEN SoldAsVacant = 1 THEN 'Yes'
	ELSE SoldAsVacant
	END
from [Nashville Housing Data for Data Cleaning];

UPDATE [Nashville Housing Data for Data Cleaning]
set SoldAsVacant2 = CASE WHEN Convert(nvarchar(5),SoldAsVacant) = 0 THEN 'No'
	WHEN Convert(nvarchar(5),SoldAsVacant) = 1 THEN 'Yes'
	ELSE Convert(nvarchar(5),SoldAsVacant)
	END;


---Remove Duplicates

select * from [Nashville Housing Data for Data Cleaning] order by UniqueID;

with RownNumCTE AS(
select * , 
ROW_NUMBER() OVER(
PARTITION BY ParcelID,
			 PropertyAddress,
			 SaleDate,
			 SalePrice, 
			 LegalReference
			 ORDER BY UniqueID)
			  as row_num
from [Nashville Housing Data for Data Cleaning]
)
select * from RownNumCTE
where row_num >1
--order BY PropertyAddress;


--- To Delete Unused Columns

select * from [Nashville Housing Data for Data Cleaning];

--ALTER TABLE [Nashville Housing Data for Data Cleaning]
--DROP COLUMN PropertyAddress, OwnerAddress, TaxDistrict, SaleDate;

