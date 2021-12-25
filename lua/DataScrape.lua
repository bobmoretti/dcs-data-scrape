do
    local csvfile = nil
    function DataScrapeExportStart()
        csvfile = io.open(lfs.writedir()..'/log.csv', 'w')
        log.write('DATA SCRAPER', log.INFO, 'starting.')
        csvfile:write('time,altMsl,tas,vvi,mach,ias,alpha,nx,ny,nz,x,y,z\n')
    end

    function DataScrapeExportData()
        local t = LoGetModelTime()
        local selfData = LoGetSelfData()
        if selfData then
            local altMsl = LoGetAltitudeAboveSeaLevel()
            local tas = LoGetTrueAirSpeed()
            local vvi = LoGetVerticalVelocity()
            local mach = LoGetMachNumber()
            local ias = LoGetIndicatedAirSpeed()
            local alpha = LoGetAngleOfAttack()
            local accel = LoGetAccelerationUnits()
            
            local allVals = {t,
                             altMsl,
                             tas,
                             vvi,
                             mach,
                             ias,
                             alpha,
                             accel.x,
                             accel.y,
                             accel.z,
                             selfData.Position.x,
                             selfData.Position.y,
                             selfData.Position.z
                            }
            for idx, value in ipairs(allVals) do
                allVals[idx] = string.format('%e', value)
                if allVals[idx] == nil then
                    allVals[idx] = '0'
                end
            end
            local line = table.concat(allVals, ',')
            csvfile:write(line..'\n')
        end
    end

    function DataScrapeExportStop()
        log.write('DATA SCRAPER', log.INFO, 'closing.')
        csvfile:close()
    end
        
    -- export start
    do
        local PrevLuaExportStart = LuaExportStart
        LuaExportStart = function()
            DataScrapeExportStart()
            if PrevLuaExportStart then
                PrevLuaExportStart()
            end
        end
    end

    -- end of frame
    do
        local PrevLuaExportAfterNextFrame = LuaExportAfterNextFrame
        LuaExportAfterNextFrame = function()
            DataScrapeExportData()
            if PrevLuaExportAfterNextFrame then
                PrevLuaExportAfterNextFrame()
            end
        end
    end

    -- end of mission (export stop)
    do
        local PrevLuaExportStop = LuaExportStop
        LuaExportStop = function()
            DataScrapeExportStop()
            if PrevLuaExportStart then
                PrevLuaExportStart()
            end
        end
    end

end

