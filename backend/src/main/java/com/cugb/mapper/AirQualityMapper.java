package com.cugb.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.cugb.entity.AirQuality;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.time.LocalDate;
import java.util.List;

@Mapper
public interface AirQualityMapper extends BaseMapper<AirQuality> {
    
    @Select("SELECT * FROM air_quality WHERE city_code = #{cityCode} AND date BETWEEN #{startDate} AND #{endDate} ORDER BY date")
    List<AirQuality> selectByCityAndDateRange(@Param("cityCode") String cityCode, 
                                               @Param("startDate") LocalDate startDate, 
                                               @Param("endDate") LocalDate endDate);
    
    @Select("SELECT * FROM air_quality WHERE date = #{date} ORDER BY aqi DESC")
    List<AirQuality> selectByDateOrderByAqiDesc(LocalDate date);
    
    @Select("SELECT * FROM air_quality WHERE date = #{date} ORDER BY aqi ASC")
    List<AirQuality> selectByDateOrderByAqiAsc(LocalDate date);
}
