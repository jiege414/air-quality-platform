package com.cugb.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.cugb.entity.AirQuality;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.time.LocalDate;
import java.util.List;
import java.util.Map;

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
    
    /**
     * 从air_quality表中获取所有城市列表（去重）
     */
    @Select("SELECT DISTINCT city_code as cityCode, city_name as cityName FROM air_quality ORDER BY city_code")
    List<Map<String, Object>> selectAllCities();
    
    /**
     * 从air_quality表中模糊搜索城市
     */
    @Select("SELECT DISTINCT city_code as cityCode, city_name as cityName FROM air_quality WHERE city_name LIKE CONCAT('%', #{keyword}, '%') OR city_code LIKE CONCAT('%', #{keyword}, '%') ORDER BY city_code")
    List<Map<String, Object>> searchCities(@Param("keyword") String keyword);
}
